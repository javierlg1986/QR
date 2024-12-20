# -*- coding: utf-8 -*-

from PIL import Image
from datetime import datetime
from urllib.parse import unquote_plus
from os import makedirs

from app import app
from app.back.aux_.db import get_db

def serializado_a_diccionario(
        serializados,
        formatos_fecha=["%d/%m/%Y"],
        multivalor=None
        ):
    resultado = {}
    if not serializados:
        return {
            "status_code": 403,
            "error": "Non se editou ningún dato",
            "codigo_error": 403}
    for par in serializados.split("&"):
        clave, valor = par.split("=")
        clave = unquote_plus(clave)
        valor = unquote_plus(valor)
        if 'fecha' in clave:
            formato_fecha_valido = 0
            for formato_fecha in formatos_fecha:
                try:
                    valor = int(datetime.strptime(valor, formato_fecha).timestamp())
                    formato_fecha_valido = 1
                    break
                except:
                    pass
            if not formato_fecha_valido:
                formato_fecha_texto = str(formatos_fecha)
                formato_fecha_texto = formato_fecha_texto.replace("%d", "dd")
                formato_fecha_texto = formato_fecha_texto.replace("%m", "mm")
                formato_fecha_texto = formato_fecha_texto.replace("%Y", "aaaa")
                formato_fecha_texto = formato_fecha_texto.replace("%H", "hh")
                formato_fecha_texto = formato_fecha_texto.replace("%M", "mm")
                return {"status_code": 403,
                        "error": "Comprobe que a data ten "
                                + f"o formato {formato_fecha_texto}.",
                        "codigo_error": 403
                        }
        if multivalor and resultado[clave]:
            if type(resultado[clave]) is not list:
                resultado[clave] = [
                    resultado[clave]
                    ]
            else:
                resultado[clave].append(valor)
        else:
            resultado.update({clave: valor})
    resultado.update({"status_code": 200})
    return resultado

def obten_columnas(cur, tabla):
    cur.execute("PRAGMA table_info({})".format(tabla))
    datos = cur.fetchall()
    columnas_BD = {}
    for dato in datos:
        columnas_BD.update({dato['name']: dato['type']})
    return columnas_BD

def actualiza_BBDD_diccionario(
        diccionario,
        tabla,
        id_elemento,
        lista_prohibidos=['id'],
        campos_js=[]
        ):
    db = get_db()
    cur = db.cursor()

    SQL_string = f"UPDATE {tabla} SET"

    if diccionario:
        columnas = obten_columnas(cur, tabla)
        lista_valores = []
        for key in diccionario:
            if key not in columnas:
                return {
                    "status_code": 400,
                    "error": "[KEY] Hay datos que no se pueden actualizar.",
                    'codigo_erro': 400
                    } 
            if key in lista_prohibidos:
                return {
                    "status_code": 400,
                    "error": "[JS] Hay datos que no se pueden actualizar.",
                    'codigo_erro': 400
                    } 
            if key in campos_js\
                and any(elem in key for elem in "\"\'();$%&@!"):
                return {
                    "status_code": 400,
                    "error": "Los siguientes campos: {} no pueden tener caracteres especiales. Sustitúyalos e inténtelo de nuevo.".format(campos_js),
                    'codigo_erro': 400
                    } 
            SQL_string += " {} = ?,".format(key)
            valor = diccionario[key]
            if columnas[key] == 'FLOAT':
                valor = valor.replace(",", ".")
            lista_valores.append(valor)
        SQL_string = SQL_string[:-1] + " WHERE id = ?"
        lista_valores.append(id_elemento)
        cur.execute(SQL_string, tuple(lista_valores))
    db.commit()
    return {"status_code": 200}


def ordena_diccionario_vinculado(diccionario: dict):
    """Toma un diccionario cuyas claves tienen la forma:
    <id>|<clave> y devuelven un diccionario de la forma:
    <id>: {<clave>: <parametro>}
    """
    resultado = {}
    for key, valor in diccionario.items():
        id_tabla, clave = key.split("|")
        if id_tabla not in resultado:
            resultado[id_tabla] = {}
        resultado[id_tabla].update({
            clave: valor
        })
    return resultado


def id_vinculados(tabla, id_tabla_principal, clave_foranea):
    """Obtiene un listado de id de una tabla vinculada a una principal.
    Por ejemplo, listado de id de fotos con mismo id_inspeccion_elem_red;
    listado id de inspecciones para un id_elemento_red
    """
    db = get_db()
    cur = db.cursor()
    cur.execute((f"""
        SELECT t.id
        FROM {tabla} t
        WHERE {clave_foranea} = ? 
        """), (id_tabla_principal,))
    lista_id_vinc = lista_id(cur.fetchall(), lista=1)
    return lista_id_vinc


def sqliteRow2list_dict(sqliteRow):
    """Toma una lista de sqliteRows (resultado de un fetchall) y lo convierte
    a una lista de diccionarios de python.
    """
    resultado = []
    for elemento in sqliteRow:
        subresultado = {}
        for key in elemento.keys():
            subresultado.update({key:elemento[key]})
        resultado.append(subresultado)
    return resultado


def sqliteRow2dict_dict(sqliteRow, columna='id'):
    """Toma una lista de sqliteRows (resultado de un fetchall) y lo convierte
    a un diccionario cuyas claves son la columna (por defecto id) y los
    valores son un diccionario con el resto de columnas.
    """
    resultado = {}
    for elemento in sqliteRow:
        subresultado = {}
        for key in elemento.keys():
            subresultado.update({key:elemento[key]})
        resultado.update({elemento[columna]: subresultado})
    return resultado


def lista_id(sqliteRow, campo='id', lista=0):
    """Dado un sqliteRow, devuelve por defecto un string de los valores del
    campo separados por comas, listo para ser usado en una query.
    Si no se incluye un nombre de campo, devuelve el campo 'id'.
    Opcionalmente, puede devolver una lista
    """
    listado = []
    for elemento in sqliteRow:
        if str(elemento[campo]) not in listado:
            listado.append(str(elemento[campo]))
    if not lista:
        resultado = ", ".join(listado)
    else:
        resultado = listado
    return resultado


ALLOWED_EXTENSIONS = {
    'doc': 'pdf',
    'img': ['png', 'jpg', 'jpeg']
    }


def allowed_file(filename, type):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS[type]


def creaThumbnail(directorio, archivo, tamano=300):
    image = Image.open(f"{directorio}{archivo}")
    makedirs(f'{directorio}tn/', exist_ok=True)
    MAX_SIZE = (tamano, tamano)
    image.thumbnail(MAX_SIZE)
    image.save(f'{directorio}tn/{archivo}')