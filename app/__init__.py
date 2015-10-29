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
        print("Created DB/tables")
        db.create_all()

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
