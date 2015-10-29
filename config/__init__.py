#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Configurations """

import os, json

CONFIG_PATH = 'config'
JSON_EXT = 'json'
PATH = 'base'


########################################
# Read user config
def read_files(path):
    """ All user specifications """

    # The HTML content
    section = 'content'
    filename = os.path.join(CONFIG_PATH, path, section + "." + JSON_EXT)
    myjson = {}
    with open(filename) as f:
        myjson[section] = json.load(f)
    # Logo image
    myjson[section]['logopath'] = os.path.join('/static/img/logo.png')
    return myjson

user_config = read_files(PATH)


########################################
class BaseConfig(object):

    DEBUG = False
    TESTING = False

    SECRET_KEY = 'my precious'
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + \
        os.path.join(BASE_DIR, 'database.db')

    HOST = 'localhost'
    PORT = int(os.environ.get('PORT', 5000))


class DevelopmentConfig(BaseConfig):

    DEBUG = True
    HOST = '0.0.0.0'

    WTF_CSRF_SECRET_KEY = 'a random string'

    # We have POSTGRESQL. Use docker environment variables
    dbdriver = "postgresql"
    dbhost = os.environ["DB_NAME"].split('/')[2]
    dbport = int(os.environ["DB_PORT"].split(':')[2])
    dbuser = os.environ["DB_ENV_POSTGRES_USER"]
    dbpw = os.environ["DB_ENV_POSTGRES_PASSWORD"]
    database = os.environ["DB_ENV_POSTGRES_DB"]

    SQLALCHEMY_DATABASE_URI = "%s://%s:%s@%s:%d/%s" \
        % (dbdriver, dbuser, dbpw, dbhost, dbport, database)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
