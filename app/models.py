#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Database models """

#############################################
# DB INIT
from flask.ext.sqlalchemy import SQLAlchemy
# no app object passed! Instead we use use db.init_app in the factory.
db = SQLAlchemy()

#############################################
# Convert an SQLALCHEMY model into a Flask table

from flask_table import Table, Col, create_table
from sqlalchemy import inspect

class ItemTable(Table):
    def thead(self):
        return '<thead class="thead-default"><tr>{}</tr></thead>'\
            .format(''.join( (self.th(col_key, col) \
            for col_key, col in self._cols.items() if col.show)))

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
    #print("Table:", table_name)

    mapper = inspect(obj)
    for column in mapper.attrs:
        colname = column.key.replace('_', ' ').capitalize()
        #print("SQLALCHEMY col", colname)
        TableCls.add_column(column.key, Col(colname))

    TableCls.classes = ['table', 'table-striped', 'table-hover']

    return TableCls

#############################################
# Work on models

from wtforms.validators import Email, Length
from wtforms import PasswordField

class MyModel(db.Model):
    ## Primary key
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    ## Normal
    name = db.Column(db.Unicode(5), nullable=False, \
        info={'validators': Length(min=5,max=255)})
    ## Custom validator
    email = db.Column(db.Unicode(255), nullable=False, info={'validators': Email()})
    ## Test SELECT
    # enum sqlalchemy tutorial http://techspot.zzzeek.org/2011/01/14/the-enum-recipe/
    test_select_a = db.Column(db.Enum('part_time', 'full_time', 'contractor', name='employee_types'))
    # test_select_b = db.Column(db.Integer, \
    #     info={'choices': [(i, i) for i in range(13, 99)]}, nullable=False)
    ## Password field from WTForm types
    password = db.Column(db.String(255), info={'form_field_class': PasswordField} )

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
