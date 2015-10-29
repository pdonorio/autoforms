#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Factory and blueprints patterns """

import os, logging
from flask import Flask, request as req
from .pages import blueprint

config = {
    "development": "config.DevelopmentConfig",
    # "testing": "bookshelf.config.TestingConfig",
    "default": "config.DevelopmentConfig"
}

# // TO FIX:
# move this data into json
# also: should i read json files here? and save them as global
# with flask g?

# First column empty for auto-increment
data = [
    "-;FEXS0;adult;A001;IT;caucasian;29;male;168;3-10;60;;-;maternal;yes;1-5;yes;4;II;3;BOTH;1;UPPER LIMBS;;no;yes;right proximal femur;25;;;;no;diabetes;neurofibromatosis;yes;EXT1;c.1831A>T;p.Lys611*;nonsense;",
    "-;FEXS0;child;A001;;;7;male;125;50-75;-;;positive;maternal;yes;7;yes;7;I;0;;0;;;no;;;;;;;;diabetes;neurofibromatosis;yes;EXT1;1165(-2)A>-G;;splicesite;",
    "-;FEXS0;child;A001;;;9;male;127;25-50;-;;positive;maternal;yes;9;yes;8;I;0;;0;;;no;;;;;;;;diabetes;neurofibromatosis;yes;EXT1;1165(-2)A>-G;;splicesite;",
]

def myinsert(db, data):

    from sqlalchemy import inspect
    from .models.mo import MyModel

    for row in data:
        pieces = row.split(';')
        mapper = inspect(MyModel)
        i = 0
        content = {}
        for column in mapper.attrs:
            try:
                value = pieces[i]
                if not (value == '-' or value.strip() == ''):
                    content[column.key] = pieces[i]
            except:
                pass
            i += 1

        obj = MyModel(**content)
        db.session.add(obj)
        db.session.commit()


def create_app(config_filename):
    """ Create the istance for Flask application """
    app = Flask(__name__)

    # Apply configuration
    config_name = os.getenv('FLASK_CONFIGURATION', 'default')
    app.config.from_object(config[config_name])

    # # Cache
    # # http://flask.pocoo.org/docs/0.10/patterns/caching/#setting-up-a-cache
    # from werkzeug.contrib.cache import SimpleCache
    # cache = SimpleCache()

    # Database
    from .basemodel import db
    db.init_app(app)

    # Add things to this app
    app.register_blueprint(blueprint)
    app.logger.setLevel(logging.NOTSET)

    # Application context
    with app.app_context():
        # Extensions like Flask-SQLAlchemy now know what the "current" app
        # is while within this block. Therefore, you can now run........
# // TO FIX:
# Drop tables and populate with basic data, only on request
# e.g. startup option
        db.drop_all()
        print("Created DB/tables")
        db.create_all()
        myinsert(db, data)

# SANITY CHECKS?
        # from .sanity_checks import is_sane_database
        # from .models import MyModel
        # # Note, this will check all models, not only MyModel...
        # is_sane_database(MyModel, db.session)

    # Logging
    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(req.method,req.url,req.data,resp))
        return resp

    return app
