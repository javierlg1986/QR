# -*- coding: utf-8 -*-
from flask import session, jsonify, render_template, request
from os import path, makedirs
from datetime import datetime
import uuid
import qrcode
import base64
from io import BytesIO

from app import app
from app.back.aux_.auditoria import log_db
from app.back.aux_.seguridad import permiso
from app.back.aux_.db import get_db
from app.back.aux_.tools import allowed_file, creaThumbnail
from app.back.aux_.config import app_conf
from app.back.aux_.tools import sqliteRow2list_dict
import configparser

config_url = configparser.ConfigParser()
config_url.read('configuracion.conf')
url_QR=config_url['app_conf']['url_QR']
 

@app.route('/_crea_QR_db', methods=['GET', 'POST'])
@permiso
def _crea_QR_db():
    db = get_db()
    cur = db.cursor()
    fecha = datetime.now().replace(
        microsecond=0
        ).timestamp()
    id_usuario = session.get('id_usuario')
    cur.execute("""
        INSERT INTO QR
        (fecha, id_usuario)
        VALUES (?, ?)
        """, (fecha, id_usuario))
    db.commit()
    id_QR = cur.lastrowid
    token_QR = crea_token_QR(id_QR)
    actualiza_token_QR(token_QR, id_QR)
    QR_db_info = QR_db_por_token(token_QR)
    log_db("QR", id_QR, "C", token_QR)
    return QR_db_info

@app.route('/_crea_QR_imagen/<string:token_QR_request>', methods=['GET','POST'])
@permiso
def _crea_QR_imagen(token_QR_request):
    url = url_QR+str(token_QR_request)
    imagen_QR = qrcode.make(url)
    buffered = BytesIO()
    imagen_QR.save(buffered, format="PNG")
    imagen_QR_base_64 = base64.b64encode(buffered.getvalue()).decode()
    return imagen_QR_base_64

@app.route('/_borra_QR_db/<string:token_QR_request>', methods=['GET','POST'])
@permiso
def _borra_QR_db(token_QR_request):
    token_QR = token_QR_request
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        DELETE FROM QR
        WHERE tokenQR = ?
        """, (token_QR,))
    db.commit()
    log_db("QR", token_QR, "D", token_QR)
    return jsonify({
        'token_QR': token_QR,
        })

@app.route('/_listado_elementos_sin_QR_db', methods=['POST'])
@permiso
def _listado_elementos_sin_QR_db():
    listado_elementos_sin_QR=[]
    db = get_db()
    cur = db.cursor()
    lista_tablas = sqliteRow2list_dict(cur.execute("""
        Select * FROM lista_tablas
        """).fetchall())
    db.commit()

    query=''
    elementos_inventario=[]
    elemento_test={}
    nombre_tabla=''
    id_test=0

    for tabla in lista_tablas:
        db = get_db()
        cur = db.cursor()
        elementos_inventario = sqliteRow2list_dict((cur.execute('Select * FROM {}'.format(tabla['nombre_tabla']))).fetchall())
        db.commit()
        for elemento in elementos_inventario:
            db = get_db()
            cur = db.cursor()
            selector = sqliteRow2list_dict(cur.execute("""
                Select * FROM QR
                WHERE tabla_asignada = ? AND id_elem_en_tabla_asig = ?
                """, (tabla['id'], elemento['id'])).fetchall())
            if selector:
                elemento['tokenQR'] = selector[0]['tokenQR']
            if  'tokenQR' not in elemento.keys():
                elemento['id_tabla'] = tabla['id']
                listado_elementos_sin_QR.append(elemento)
    return  listado_elementos_sin_QR

@app.route('/_listado_QR_sin_asignar', methods=['POST'])
@permiso
def _listado_QR_sin_asignar():
    return "OK"

@app.route('/_asigna_QR_inv', methods=['POST'])
@permiso
def _asigna_QR_inv():
    token_QR_request = request.form.get('token_QR_request')
    tabla_request = request.form.get('tabla_request')
    id_en_tabla_request = request.form.get('id_en_tabla_request')
    
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE QR
        SET tabla_asignada = ?, id_elem_en_tabla_asig = ?
        WHERE tokenQR = ?
        """, (tabla_request, id_en_tabla_request, token_QR_request))
    db.commit()
    # log_db("QR", token_QR_request, "U", tabla_request)
    # log_db("QR", token_QR_request, "U", id_en_tabla_request)
    return jsonify({
        'token_QR': token_QR_request,
        'tabla_asignada': tabla_request,
        'id_elem_en_tabla_asig': id_en_tabla_request,
        })

def QR_db_por_token(token_QR_request):
    token_QR = token_QR_request
    db = get_db()
    cur = db.cursor()
    QR_leido = sqliteRow2list_dict(cur.execute("""
        Select * FROM QR
        WHERE tokenQR = ?
        """, (token_QR,)).fetchall())[0]
    db.commit()
    return QR_leido

def QR_db_por_id(id_QR_request):
    id_QR = id_QR_request
    db = get_db()
    cur = db.cursor()
    QR_leido = sqliteRow2list_dict(cur.execute("""
        Select * FROM QR
        WHERE id = ?
        """, (id_QR,)).fetchall())[0]
    db.commit()
    return QR_leido

def crea_token_QR(id_QR):
    token_QR_uuid=uuid.uuid4().hex
    return token_QR_uuid

def actualiza_token_QR(token_QR_actualizar, id_QRactualizar):
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        UPDATE QR
        SET tokenQR = ?
        WHERE id = ?
        """, (token_QR_actualizar, id_QRactualizar))
    db.commit()
    return

def obtener_token_QR_de_id_QR(id_QR_request):
    db = get_db()
    cur = db.cursor()
    QR_leido = sqliteRow2list_dict(cur.execute("""
        Select tokenQR FROM QR
        WHERE id = ?
        """, (id_QR_request,)).fetchall())[0]
    db.commit()
    return QR_leido['tokenQR']

def obtener_id_QR_de_token_QR(token_QR_request):
    db = get_db()
    cur = db.cursor()
    QR_leido = sqliteRow2list_dict(cur.execute("""
        Select id FROM QR
        WHERE tokenQR = ?
        """, (token_QR_request,)).fetchall())[0]
    db.commit()
    return QR_leido['id']

def guardar_QR_img(imagen, nombre_imagen):
    directorio = f"{app_conf.ruta}front/static_priv/QR/"
    makedirs(directorio, exist_ok=True)
    ruta = nombre_imagen+".jpg"
    if imagen and allowed_file(nombre_imagen, 'img'):
        try:
            imagen.save(path.join(directorio, ruta))
            creaThumbnail(directorio, ruta)
        except Exception as e:
            log(exito=0)
            return jsonify({
                "error": "Erro gardando o ficheiro."
            }), 400

