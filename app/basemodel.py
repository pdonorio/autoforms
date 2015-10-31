#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Database models """

from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_table import Table, Col  # , create_table
from flask import url_for, request
from sqlalchemy import inspect
from collections import OrderedDict

#############################################
# DB INIT
# no app object passed! Instead we use use db.init_app in the factory.
db = SQLAlchemy()
# Flask LOGIN
lm = LoginManager()

# from flask.ext.openid import OpenID
# oid = OpenID()

#############################################
# Convert an SQLALCHEMY model into a Flask table
class AnchorCol(Col):
    def td_format(self, content):
        return '<a href="/view/' + content + '">' + content + '</a>'


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

def model2list(obj):
    mylist = []
    for column in inspect(obj).attrs:
        mylist.append(column.key)
    return mylist

def model2table(obj, selected):
    """ Give me an SQLALCHEMY obj to get an HTML table """

    table_name = 'Table' + obj.__name__
    TableCls = create_table(table_name)
    mapper = inspect(obj)

    for column in mapper.attrs:

        # What to skip
        if selected and column.key not in selected:
            continue

        colname = column.key.replace('_', ' ').capitalize()
        if column.key == 'id':  # 'patient_id':
            TableCls.add_column(column.key, AnchorCol(colname))
        else:
            TableCls.add_column(column.key, Col(colname))

    TableCls.classes = ['table', 'table-hover']
    TableCls.allow_sort = True

    return TableCls


# http://piotr.banaszkiewicz.org/blog/2012/06/30/serialize-sqlalchemy-results-into-json/ 
class DictSerializable(object):
    """ An object to keep an ordered version of ORM model attributes """
    def _asdict(self):
        result = OrderedDict()
        for key in self.__mapper__.c.keys():
            result[key] = getattr(self, key)
        return result


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

###############################################

from datetime import datetime

class User(db.Model):

    __tablename__ = "users"

    id = db.Column('user_id',db.Integer , primary_key=True)
    username = db.Column('username', db.String(20), unique=True , index=True)
    password = db.Column('password' , db.String(20))
    email = db.Column('email',db.String(50),unique=True , index=True)
    registered_on = db.Column('registered_on' , db.DateTime)

    def __init__(self , username ,password , email):
        self.username = username
        self.password = password
        self.email = email
        self.registered_on = datetime.utcnow()

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)
