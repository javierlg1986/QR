# -*- coding: utf-8 -*-

import configparser


def get_config():
    config = configparser.ConfigParser()
    config.read('configuracion.conf')
    return config


def write_config(config):
    with open('configuracion.conf', 'w') as configfile:
        config.write(configfile)


class app_conf():
    config = get_config()
    nombre = config['app_conf']['nombre']
    ruta = config['app_conf']['ruta']
    version = config['app_conf']['version']
    contacto = config['app_conf']['contacto']