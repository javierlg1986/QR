# -*- coding: utf-8 -*-

from flask import render_template, url_for, request, session, redirect, g
from datetime import datetime
import hashlib
from secrets import token_urlsafe

from app import app, Config
from app.back.aux_.db import get_db
from app.back.aux_.auditoria import log, remote_ip
from app.back.aux_.config import app_conf


@app.route('/login/<url>', methods=['GET', 'POST'])
@app.route('/login/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login(url=None):
    g.app_name = Config.app_name
    log(ip=remote_ip())
    resultados = {}
    error = None
    resultados.update({
        "contacto": app_conf.contacto,
        "app": app_conf.nombre,
        "version": app_conf.version
        })
    url_redireccion = '' if url == None else url
    if request.method == 'POST':
        usuario = request.form['username']
        contrasena = request.form['password']
        hash_form = hashlib.sha1()
        hash_form.update(contrasena.encode('utf-8'))
        contrasena_form = hash_form.hexdigest()

        db = get_db()
        cur = db.cursor()
        cur.execute("""
            SELECT 
                id,
                pass,
                administrador,
                permiso,
                bloqueado
            FROM usuarios
            WHERE usuario like ?""", (usuario,))
        usuario_DB = cur.fetchone()
        try:
            contrasena_guardada = usuario_DB['pass']
        except:
            contrasena_guardada = ""
        if contrasena_form != contrasena_guardada:
            error = 'Erro no usuario ou no password.'
        elif usuario_DB['bloqueado']:
            error = 'Usuario bloqueado. Contacte co administrador'
        else:
            session['logged_in'] = True
            session['username'] = usuario.upper()
            session['administrador'] = usuario_DB['administrador']
            session['permiso'] = usuario_DB['permiso']
            session['id_usuario'] = usuario_DB['id']
            
            this_login = datetime.now().replace(microsecond=0)
            session['last_login'] = session.get('this_login')
            session['this_login'] = this_login
            
            session['TOKEN'] = token_urlsafe()
            session.permanent = True
            return redirect("/" + url_redireccion)
    
    return render_template(
        'html/web/login/index.html',
        error=error,
        url={"url": url_for("login", url=url)},
        resultados=resultados
        )


@app.route('/logout')
def logout():
    log(ip=remote_ip())
    session.pop('logged_in', None)
    return redirect('/login')
