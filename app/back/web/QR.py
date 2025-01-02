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
from app.back.db.QR import QR_db_por_token, _crea_QR_imagen, _crea_QR_db, _listado_elementos_sin_QR_db

@app.route('/QR/<string:token_QR_request>')
@permiso
def vista_QR(token_QR_request):
    QR_db_info = QR_db_por_token(token_QR_request)
    QR_img64 = _crea_QR_imagen(token_QR_request)  

    if QR_db_info['id_elem_en_tabla_asig']!=None and QR_db_info['id_elem_en_tabla_asig']!=0 and QR_db_info['tabla_asignada']!=None and QR_db_info['tabla_asignada']!=0:
        return "redirigir a la vista del elemento asignado"
    else:
        return render_template(
            "html/web/QR/index.html",
            QR_db_info = QR_db_info,
            QR_img64 = QR_img64,
            QR_asignado = False,
        )
    
@app.route('/configurar_QR/<string:token_QR_request>')
@permiso
def vista_configurar_QR(token_QR_request):
    QR_db_info = QR_db_por_token(token_QR_request)
    QR_img64 = _crea_QR_imagen(token_QR_request)   
    
    if QR_db_info['id_elem_en_tabla_asig']!=None and QR_db_info['id_elem_en_tabla_asig']!=0 and QR_db_info['tabla_asignada']!=None and QR_db_info['tabla_asignada']!=0:
        return render_template(
            "html/web/QR/index.html",
            QR_db_info = QR_db_info,
            QR_img64 = QR_img64,
            QR_asignado = True,
        )
    else:
        return render_template(
            "html/web/QR/index.html",
            QR_db_info = QR_db_info,
            QR_img64 = QR_img64,
            QR_asignado = False,
        )

@app.route('/_crea_QR' , methods=['POST'])
@permiso
def crea_QR():
    QR_db_info = _crea_QR_db()
    QR_img64 = _crea_QR_imagen(QR_db_info['tokenQR'])   
    return render_template(
        "html/web/QR/panel_QR.html",
        QR_db_info = QR_db_info,
        QR_img64 = QR_img64,
        QR_asignado = False,
    )

    
@app.route('/_listado_elementos_sin_QR', methods=['POST'])
@permiso
def _listado_elementos_sin_QR():
    listado_elementos_sin_QR_db=_listado_elementos_sin_QR_db()

    return render_template(
            "html/web/QR/listado_elementos_sin_QR.html",
            listado_elementos_sin_QR_db = listado_elementos_sin_QR_db,
        )
    
