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

import csv
data = []
with open('config/custom/mymodel.csv', 'r') as csvfile:
    creader = csv.reader(csvfile, delimiter=';')
    for row in creader:
        data.append(row)


def myinsert(db, data, first_user):

    from sqlalchemy import inspect
    from .basemodel import User
    from .models.mo import MyModel

    user = User(**first_user)
    db.session.add(user)

    for pieces in data:
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
    from .basemodel import db, lm  # , oid
    db.init_app(app)

    # Add things to this app
    app.register_blueprint(blueprint)
    app.logger.setLevel(logging.NOTSET)

    # Flask LOGIN
    lm.init_app(app)
    #oid.init_app(app)
    lm.login_view = '.login'

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
        myinsert(db, data, app.config['BASIC_USER'])

# SANITY CHECKS?
        # from .sanity_checks import is_sane_database
        # from .models import MyModel
        # # Note, this will check all models, not only MyModel...
        # is_sane_database(MyModel, db.session)

    # Logging
    @app.after_request
    def log_response(resp):
        app.logger.info("{} {} {}\n{}".format(
            req.method,req.url,req.data,resp))
        return resp

    return app
