# -*- coding: utf-8 -*-
from flask import session, jsonify
from os import path, makedirs, remove
from datetime import datetime
import uuid
import qrcode
import base64
from io import BytesIO
from PIL import Image

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
    _crea_QR_imagen(token_QR)
    log_db("QR", id_QR, "C", token_QR)
    return jsonify({
        'id_QR': id_QR,
        'token_QR': token_QR
        })

@app.route('/_crea_QR_imagen/<string:token_QR_request>', methods=['GET','POST'])
@permiso
def _crea_QR_imagen(token_QR_request):
    id_QR_request=obtener_id_QR_de_token_QR(token_QR_request)
    #añadir ruta a configuración
    url = url_QR+str(token_QR_request)
    nombre_archivo = "img_QR"+str(token_QR_request)+".png"
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