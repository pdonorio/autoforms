#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

import importlib
from flask import Blueprint, \
    render_template, request, flash, redirect, url_for
from app import forms
from config import user_config
from .basemodel import db, model2table
from .forms import module

MyModel = module.MyModel
blueprint = Blueprint('pages', __name__)

# ######################################################
# #http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/#caching-decorator
# from functools import wraps

# def cached(timeout=5 * 1, key='view/%s'):
#     def decorator(f):
#         @wraps(f)
#         def decorated_function(*args, **kwargs):
#             cache_key = key % request.path
#             rv = cache.get(cache_key)
#             if rv is not None:
#                 return rv
#             rv = f(*args, **kwargs)
#             cache.set(cache_key, rv, timeout=timeout)
#             return rv
#         return decorated_function
#     return decorator

######################################################
MyTable = model2table(MyModel)


def insertdb(iform, obj):
    iform.populate_obj(obj)
    # flash("Populated user %s" % dir(user), 'success')
    db.session.add(obj)
    # Save into db
    db.session.commit()


def row2dict(r):
    """ Convert a single sqlalchemy row into a dictionary """
    # http://stackoverflow.com/a/1960546/2114395
    return {c.name: str(getattr(r, c.name)) for c in r.__table__.columns}

template = 'forms/insert_search.html'


@blueprint.route('/view', methods=["GET", "POST"])
def view():
    status = "View"

    sort_field = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    field = getattr(MyModel, sort_field)
    if reverse:
        from sqlalchemy import desc
        field = desc(field)

    # SQLalchemy query (sorted)
    data = MyModel.query.order_by(field)

    items = []
    for row in data:
        items.append(row2dict(row))

    return render_template('forms/view.html',
        table=MyTable(items, sort_by=sort_field, sort_reverse=reverse),
        status=status, formname='view',
        **user_config['content'])


@blueprint.route('/insert', methods=["GET", "POST"])
def insert():
    status = "Waiting data to save"
    iform = forms.UserForm()
    if iform.validate_on_submit():
        # Handle user model
        insertdb(iform, MyModel())
        flash("User saved", 'success')
        status = "Saved"

    return render_template(template,
        status=status, form=iform, formname='insert',
        **user_config['content'])


@blueprint.route('/search', methods=["GET", "POST"])
def search():
    status = "Waiting data to search"
    iform = forms.UserForm()
    if iform.validate_on_submit():
        status = "Work in progress"
        # flash("User saved", 'success')

    return render_template(template,
        status=status, form=iform, formname='search',
        **user_config['content'])


################
# Basic interface routes ####
################

@blueprint.route('/')
@blueprint.route('/home')
def home():
    return render_template('pages/placeholder.home.html',
        **user_config['content'])

@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html',
        **user_config['content'])

@blueprint.route('/login', methods=['GET','POST'])
def login():

    form = forms.LoginForm(request.form)

#http://flask.pocoo.org/snippets/64/
# NOT WORKING?
    if form.validate_on_submit():
        flash(u'Successfully logged in as %s' % form.user.username)
        session['user_id'] = form.user.id
        print("\n\n\nLOGGED!!\n\n\n")

        # Redirect to index?
        return redirect(url_for('index'))

        # Redirect to last page accessed?
        #return form.redirect('index')
    return render_template('forms/login.html', form=form)

@blueprint.route('/register')
def register():
    form = forms.RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = forms.ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
