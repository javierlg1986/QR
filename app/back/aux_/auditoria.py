# -*- coding: utf-8 -*-

from flask import session, request
from datetime import datetime

from app import app
from app.back.aux_.db import get_db


def remote_ip():
    try:
        if request.headers.getlist("X-Forwarded-For"):
            ip = request.headers.getlist("X-Forwarded-For")[0].split(",")[0]
        else:
            ip = request.remote_addr
    except:
        ip = "unknow"
    return ip


def log(exito=1, ip=None):
    """Registro de accesos a cada URL"""
    fecha = datetime.now().replace(microsecond=0).timestamp()
    id_usuario = session.get('id_usuario')
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        INSERT INTO log_accesos (
            fecha,
            id_usuario,
            url,
            exito,
            ip
        ) VALUES (?, ?, ?, ?, ?)
        """, (fecha, id_usuario, request.path, exito, ip))
    db.commit()


def log_db(
        tabla,
        id_tabla,
        tipo,
        cambio
        ):
    db = get_db()
    cur = db.cursor()
    fecha = datetime.now().replace(microsecond=0).timestamp()
    
    cur.execute("""
        INSERT INTO log_cambios (
            id_usuario,
            fecha,
            tabla,
            id_tabla,
            tipo,
            cambio
            )
        VALUES (?, ?, ?, ?, ?, ?)""",
        (
            session['id_usuario'],
            fecha,
            tabla,
            id_tabla,
            tipo,
            cambio
            )
        )
    db.commit()
