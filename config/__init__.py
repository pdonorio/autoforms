#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Configurations """

import os, json

CONFIG_PATH = 'config'
JSON_EXT = 'json'


########################################
# Read user config
def read_files(path):
    """ All user specifications """

    # The HTML content
    file = 'content'
    filename = os.path.join(CONFIG_PATH, path, file + "." + JSON_EXT)
    myjson = {}
    with open(filename) as f:
        myjson[file] = json.load(f)
    return myjson

user_config = read_files('base')


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
