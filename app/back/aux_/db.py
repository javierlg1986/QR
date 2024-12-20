# -*- coding: utf-8 -*-

import sqlite3
from os import path
from app import app
from flask import g


def connect_db():
    """Connects to the specific database."""
    BBDD = '../QR.sqlite'
    rv = sqlite3.connect(path.join(app.root_path, BBDD))
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.conector_db = connect_db()
    return g.conector_db


def close_db(e=None):
    """If this request connected to the database, close the
    connection.
    """
    db = g.pop("sqlite_db", None)
    if db is not None:
        db.close()
