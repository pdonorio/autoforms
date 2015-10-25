#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Database models """

#############################################
# DB INIT
from flask.ext.sqlalchemy import SQLAlchemy
# no app object passed! Instead we use use db.init_app in the factory.
db = SQLAlchemy()

from wtforms.validators import Email

class User(db.Model):
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    name = db.Column(db.Unicode(1), nullable=False)
    email = db.Column(db.Unicode(255), nullable=False, info={'validators': Email()})
    password = db.Column(db.String(255))

#############################################
class TestModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

# create some models
class MyModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)

    def __init__(self, username, email):
        self.username = username
        self.email = email

    def __repr__(self):
        return '<User %r>' % self.username
