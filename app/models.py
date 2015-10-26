#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Database models """

#############################################
# DB INIT
from flask.ext.sqlalchemy import SQLAlchemy
# no app object passed! Instead we use use db.init_app in the factory.
db = SQLAlchemy()

from wtforms.validators import Email
from wtforms import PasswordField

class User(db.Model):
    # Primary key
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    # Normal
    name = db.Column(db.Unicode(5), nullable=False)
    # Custom validator
    email = db.Column(db.Unicode(255), nullable=False, info={'validators': Email()})
    # Test SELECT
    # enum sqlalchemy tutorial http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
    test = db.Column(db.Enum('part_time', 'full_time', 'contractor', name='employee_types'))
    # Password field from WTForm types
    password = db.Column(db.String(255), info={'form_field_class': PasswordField} )

# #############################################
# class TestModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)

# # create some models
# class MyModel(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True)
#     email = db.Column(db.String(120), unique=True)

#     def __init__(self, username, email):
#         self.username = username
#         self.email = email

#     def __repr__(self):
#         return '<User %r>' % self.username
