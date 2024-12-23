# -*- coding: utf-8 -*-

from flask import Flask, g
import configparser


class Config(object):
    config = configparser.ConfigParser()
    config.read('configuracion.conf')
    app_name = config['app_conf']['nombre']
    PERMANENT_SESSION_LIFETIME = int(config['flask_conf']['session_lifetime'])
    SESSION_COOKIE_SECURE=config.getboolean('flask_conf', 'cookie_secure')
    SECRET_KEY=config['flask_conf']['secret_key']
    SESSION_COOKIE_HTTPONLY=config.getboolean('flask_conf', 'cookie_httponly')
    SESSION_COOKIE_SAMESITE=config['flask_conf']['cookie_samesite']
    MAX_CONTENT_LENGTH = int(config['flask_conf']['max_content_length'])


app = Flask(
    __name__,
    template_folder='front/templates',
    static_folder='front/static'
    )
app.config.from_object(Config)


from app import back
from app import front
from app.back.aux_.db import close_db


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    
    app.teardown_appcontext(close_db)


init_app(app)
