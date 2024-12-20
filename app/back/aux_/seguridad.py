# -*- coding: utf-8 -*-

from flask import session, request, redirect, g, jsonify, send_from_directory
from os import path

from app import app
from app import Config
from app.back.aux_.db import get_db
from app.back.aux_.auditoria import log, remote_ip
from app.back.aux_.config import app_conf


def permiso(f): #TODO incluir token CSRF
    def wrap(*args, **kwargs):
        error = "" 
        if not session.get('logged_in') or 1==2:
            session.pop('username', None)
            if request.path.startswith("/_"):
                error = "Usuario non logeado, "
                + "recargue a páxina e inténteo de novo."
            else:
                log(exito=0, ip=remote_ip())
                return redirect('/login/' + request.path[1:])
        if error:
            log(exito=0, ip=remote_ip())
            return jsonify({
                "exito": 0,
                "error": error}), 401
        
        log()
        g.app_name = Config.app_name
        return f(*args, **kwargs)
    wrap.__name__ = f.__name__ + "permiso"
    return wrap


def extrae_input_usuario(elemento, diccionario, solicitud):
    valor_elemento = diccionario.get(elemento)
    if not valor_elemento:
        if solicitud.method == 'GET':
            valor_elemento = solicitud.args.get(elemento)
        elif solicitud.method == 'POST':
            valor_elemento = solicitud.form.get(elemento)
    if not valor_elemento:
        valor_elemento = solicitud.get_json().get(elemento)
    return valor_elemento


@app.route("/static_priv/<directorio>/<subdirectorio>/<archivo>")
@app.route("/static_priv/<etiqueta>/<directorio>/<subdirectorio>/<archivo>")
def static_priv(directorio, subdirectorio, archivo, etiqueta=None):
    ruta_base = 'front/static_priv/'
    ruta_error = f'{directorio}/no-image-available.png'
    if not session.get('logged_in'):
        log(exito=0, ip=remote_ip())
        return send_from_directory(ruta_base, ruta_error), 401
    ruta = f"{directorio}/{subdirectorio}/{archivo}"
    codigo_HTTP = 200
    if not path.exists(f'{app_conf.ruta}{ruta_base}{directorio}/{subdirectorio}'):
        ruta = ruta_error
        codigo_HTTP = 404
    download_name = ruta
    if etiqueta:
        download_name = etiqueta
    #TODO probar seguridad de un nombre con dos puntos y movidas raras
    return send_from_directory(
        ruta_base,
        ruta,
        as_attachment=True,
        download_name=download_name
        ), codigo_HTTP


def esFloat(cadena):
    if isinstance(cadena, list):
        for elemento in cadena:
            try:
                float(elemento)
            except:
                return 0
        return 1
    else:
        try:
            float(cadena)
            return 1
        except:
            return 0
