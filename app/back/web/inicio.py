# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request, g

from app import app, Config
from app.back.aux_.db import get_db
from app.back.aux_.seguridad import permiso
from app.back.aux_.tools import sqliteRow2dict_dict


@app.route('/')
@permiso
def index():
    db = get_db()
    cur = db.cursor()
    cur.execute("""
        SELECT *
        FROM traballos
        """)
    traballos = cur.fetchall()
    return render_template(
        "html/web/inicio/index.html",
        traballos=traballos
    )
