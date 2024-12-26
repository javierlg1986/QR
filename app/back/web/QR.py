# -*- coding: utf-8 -*-

from flask import render_template, jsonify, session, request
from datetime import datetime
import json

from app import app
from app.back.aux_.db import get_db
from app.back.aux_.auditoria import log, log_db
from app.back.aux_.seguridad import permiso, esFloat
from app.back.aux_.tools import serializado_a_diccionario,\
    actualiza_BBDD_diccionario, sqliteRow2dict_dict,\
    id_vinculados
from app.back.db.QR import obtener_id_QR_de_token_QR, QR_db_por_id, _crea_QR_imagen

@app.route('/QR/<string:token_QR_request>')
@permiso
def vista_QR(token_QR_request):
    id_QR_request = obtener_id_QR_de_token_QR(token_QR_request)
    QR_db_info = QR_db_por_id(id_QR_request)
    QR_img64 = _crea_QR_imagen(token_QR_request)
    QR_datos=json.loads(verificar_QR_asignado(token_QR_request).get_data().decode("utf-8"))
    if QR_datos['QR_asignado']==True:
        return "redirigir a aplicación inventario"
    else:
        return render_template(
            "html/web/QR/index.html",
            QR_db_info = QR_db_info,
            QR_img64 = QR_img64,
            QR_asignado = QR_datos['QR_asignado'],
        )
    
def verificar_QR_asignado(token_QR):
    QR_asignado = False
    tabla_asignada = "tabla_ejemplo"
    id_tabla_asignada = "id_tabla_ejemplo"
    return jsonify({
                "QR_asignado": QR_asignado,
                "tabla_asignada": tabla_asignada,
                "id_tabla_asignada": id_tabla_asignada,
            })