#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Database models """

from flask.ext.sqlalchemy import SQLAlchemy
from flask_table import Table, Col  # , create_table
from flask import url_for, request
from sqlalchemy import inspect

#############################################
# DB INIT
# no app object passed! Instead we use use db.init_app in the factory.
db = SQLAlchemy()


#############################################
# Convert an SQLALCHEMY model into a Flask table
class AnchorCol(Col):
    def td_format(self, content):
        return '<a href="view/' + content + '">' + content + '</a>'
    # def td_contents(self, i, attr_list):
    #     return self.td_format(self.from_attr_list(i, attr_list))


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


def model2table(obj, selected):
    """ Give me an SQLALCHEMY obj to get an HTML table """

    table_name = 'Table' + obj.__name__
    TableCls = create_table(table_name)
    # print("Table:", table_name)

    mapper = inspect(obj)
    for column in mapper.attrs:
        colname = column.key.replace('_', ' ').capitalize()
        # print("SQLALCHEMY col", colname)
        if column.key in selected:
            if column.key == 'patient_id':
                TableCls.add_column(column.key, AnchorCol(colname))
            else:
                TableCls.add_column(column.key, Col(colname))

    TableCls.classes = ['table', 'table-hover']
    TableCls.allow_sort = True

    return TableCls


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
