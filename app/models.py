#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Database models """

from flask.ext.sqlalchemy import SQLAlchemy
from flask_table import Table, Col  # , create_table
from flask import url_for, request
from sqlalchemy import inspect
from wtforms.validators import Email, Length
from wtforms import PasswordField

#############################################
# DB INIT
# no app object passed! Instead we use use db.init_app in the factory.
db = SQLAlchemy()


#############################################
# Convert an SQLALCHEMY model into a Flask table
class ItemTable(Table):

    def thead(self):
        return '<thead class="thead-default"><tr>{}</tr></thead>' \
            .format(''.join((self.th(col_key, col)
                    for col_key, col in self._cols.items() if col.show)))

    def sort_url(self, col_key, reverse=False):
        if reverse:
            direction = 'desc'
        else:
            direction = 'asc'
# // TO FIX:
# do not like the 'view' link here!
        return url_for(request.endpoint, sort=col_key, direction=direction)

# Note: bootstrap can apply label colors to row
    # def tr_format(self, item):
    #     print(item)
    #     if item.important():
    #         return ' <thead class="thead-default"><tr>{}</tr></thead>'
    #     else:
    #         return '<tr>{}</tr>'


def create_table(name):
    return type(name, (ItemTable,), {})


def model2table(obj):
    """ Give me an SQLALCHEMY obj to get an HTML table """

    table_name = 'Table' + obj.__name__
    TableCls = create_table(table_name)
    # print("Table:", table_name)

    mapper = inspect(obj)
    for column in mapper.attrs:
        colname = column.key.replace('_', ' ').capitalize()
        # print("SQLALCHEMY col", colname)
        TableCls.add_column(column.key, Col(colname))

    TableCls.classes = ['table', 'table-hover']
    TableCls.allow_sort = True

    return TableCls


#############################################
# Work on models
class MyModel(db.Model):

    # Primary key
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    # Normal
    name = db.Column(db.Unicode(5), nullable=False,
                     info={'validators': Length(min=5, max=255)})
    # Custom validator
    email = db.Column(db.Unicode(255), nullable=False,
                      info={'validators': Email()})
    # Test SELECT
    # enum sqlalchemy tutorial
    # http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
    test_select_a = db.Column(db.Enum(
        'part_time', 'full_time', 'contractor', name='employee_types'))
    # Password field from WTForm types
    password = db.Column(db.String(255),
                         info={'form_field_class': PasswordField})

MyTable = model2table(MyModel)

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
