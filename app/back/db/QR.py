# -*- coding: utf-8 -*-
from flask import session, jsonify
from datetime import datetime
import uuid
import qrcode
from PIL import Image

from app import app
from app.back.aux_.auditoria import log_db
from app.back.aux_.seguridad import permiso
from app.back.aux_.db import get_db
from app.back.aux_.config import app_conf
from app.back.aux_.tools import sqliteRow2list_dict

# Funcionalidad para la creación (y borrado, a decidir) de códigos QR y sus token asociados. Tomado como plantilla crear foto, a elaborar.
class CodigoQR():
    def __init__(self, data, nombre_archivo):
        self.data = data
        self.nombre_archivo = nombre_archivo

    def generar_qr(self):
        imagen = qrcode.make(self.data)
        nombre_archivo = self.nombre_archivo
        imagen.save(nombre_archivo)
        Image.open(nombre_archivo).show()

@app.route('/_crea_QR_db', methods=['POST'])
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
    log_db("QR", id_QR, "C", token_QR)
    return jsonify({
        'id_QR': id_QR,
        'token_QR': token_QR
        })

@app.route('/_crea_QR_imagen/<int:id_QR_request>', methods=['GET','POST'])
@permiso
def _crea_QR_imagen(id_QR_request):
    id_QR = id_QR_request
    #añadir a configuración
    url = "https://auditorias.rexega.com/rede-PADR-"+str(id_QR)
    nombre_archivo = "imagen_codigo"+str(id_QR)+".png"
    qr_generador = CodigoQR(url, nombre_archivo)
    qr_generador.generar_qr()

    return jsonify({
        'id_QR': id_QR
        })

@app.route('/_borra_QR_db/<int:id_QR_request>', methods=['GET','POST'])
@permiso
def _borra_QR_db(id_QR_request):
    id_QR = id_QR_request
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        DELETE FROM QR
        WHERE id = ?
        """, (id_QR,))
    db.commit()
    log_db("QR", id_QR, "D", id_QR)
    return jsonify({
        'id_QR': id_QR,
        })

@app.route('/_QR_db/<int:id_QR_request>')
@permiso
def _QR_db(id_QR_request):
    id_QR = id_QR_request
    db = get_db()
    cur = db.cursor()
    QR_leido = sqliteRow2list_dict(cur.execute("""
        Select * FROM QR
        WHERE id = ?
        """, (id_QR,)).fetchall())
    db.commit()
    return jsonify(QR_leido[0])

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


