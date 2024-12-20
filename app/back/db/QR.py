# -*- coding: utf-8 -*-

from flask import jsonify, request, render_template
from os import path, makedirs, remove
from werkzeug.utils import secure_filename
from datetime import datetime

from app import app
from app.back.aux_.auditoria import log, remote_ip, log_db
from app.back.aux_.seguridad import permiso
from app.back.aux_.db import get_db
from app.back.aux_.tools import allowed_file, creaThumbnail
from app.back.aux_.config import app_conf
from app.back.aux_.constants import TABLAS

# Funcionalidad para la creación (y borrado, a decidir) de códigos QR y sus token asociados. Tomado como plantilla crear foto, a elaborar.

# @app.route('/_crea_foto', methods=['POST'])
# @permiso
# def _crea_foto():
#     tabla = request.form.get("tabla")
#     id_tabla = request.form.get("id_tabla")
#     etiqueta = request.form.get("etiqueta")
#     editar = request.form.get("editar")
#     if 'file' not in request.files:
#         log(exito=0, ip=remote_ip())
#         return jsonify({
#             "error": "Non se atopa a foto."
#         }), 400
#     file = request.files.get('file')
#     if tabla not in TABLAS:
#         log(exito=0, ip=remote_ip())
#         return jsonify({
#              "error": "Táboa incorrecta."
#         }), 400
#     db = get_db()
#     cur = db.cursor()
#     cur.execute(f"""
#         INSERT INTO fotos_{TABLAS[tabla][0]}
#         ({TABLAS[tabla][1]}, etiqueta)
#         VALUES (?, ?)
#         """, (id_tabla, etiqueta))
#     id_foto = cur.lastrowid
#     fecha = datetime.now().strftime("%Y%m%d")
#     ruta = f"{fecha}_{tabla[:1]}{id_tabla}_{id_foto}.jpg"
#     cur.execute(f"""
#         UPDATE fotos_{TABLAS[tabla][0]}
#         SET ruta = ?
#         WHERE id = ?
#         """, (ruta, id_foto))
#     directorio = f"{app_conf.ruta}front/static_priv/fotos/{tabla}/"
#     makedirs(directorio, exist_ok=True)
#     if file and allowed_file(file.filename, 'img'):
#         try:
#             file.save(path.join(directorio, ruta))
#             db.commit()
#             creaThumbnail(directorio, ruta)
#         except Exception as e:
#             db.close()
#             log(exito=0)
#             return jsonify({
#                 "error": "Erro gardando o ficheiro."
#             }), 400

#     nueva_foto = render_template(
#         "html/web/common/foto.html",
#         foto={
#             "id": id_foto,
#             "etiqueta": etiqueta,
#             "ruta": ruta
#         },
#         tabla=tabla,
#         id_tabla=id_tabla,
#         editar=int(editar)
#     )
#     log_db(f"fotos_{TABLAS[tabla][0]}", id_foto, "C", None)
#     return jsonify({"nueva_foto": nueva_foto})


# @app.route("/_borra_foto", methods=['POST'])
# @permiso
# def _borra_foto():
#     id_foto = request.form.get('id_foto')
#     tabla = request.form.get('tabla')
#     if tabla not in TABLAS:
#         log(exito=0, ip=remote_ip())
#         return jsonify({
#              "error": "Táboa incorrecta."
#         }), 400
#     db = get_db()
#     cur = db.cursor()
#     cur.execute(f"""
#         SELECT ruta
#         FROM fotos_{TABLAS[tabla][0]}
#         WHERE id = ?
#         """, (id_foto,))
#     ruta = cur.fetchone()['ruta']
#     directorio = f"{app_conf.ruta}front/static_priv/fotos/{tabla}/"
#     try:
#         remove(path.join(directorio, ruta))
#         remove(path.join(directorio, 'tn/', ruta))
#     except Exception as e:
#         log(exito=0)
#     cur.execute(f"""
#         DELETE FROM fotos_{TABLAS[tabla][0]}
#         WHERE id = ?
#         """, (id_foto,))
#     db.commit()
#     log_db(f"fotos_{TABLAS[tabla][0]}", id_foto, "D", ruta)
#     return jsonify()