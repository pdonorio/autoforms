#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" App MAIN """

from app import create_app
from config import DevelopmentConfig
app = create_app(DevelopmentConfig)

if __name__ == '__main__':
    host = app.config.get("HOST")
    port = app.config.get("PORT")
    app.run(host=host, port=port)
