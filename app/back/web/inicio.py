# -*- coding: utf-8 -*-

from flask import render_template, jsonify, request, g

from app import app, Config
from app.back.aux_.seguridad import permiso

@app.route('/')
@permiso
def index():
    return render_template(
        "html/web/inicio/index.html",
    )
