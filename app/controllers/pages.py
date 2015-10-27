#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

from flask import current_app, Blueprint, \
    render_template, request, flash, redirect, url_for
from app import forms

blueprint = Blueprint('pages', __name__)

######################################################
#http://flask.pocoo.org/docs/0.10/patterns/viewdecorators/#caching-decorator
from functools import wraps
from flask import request

def cached(timeout=5 * 1, key='view/%s'):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            cache_key = key % request.path
            rv = cache.get(cache_key)
            if rv is not None:
                return rv
            rv = f(*args, **kwargs)
            cache.set(cache_key, rv, timeout=timeout)
            return rv
        return decorated_function
    return decorator

######################################################
## PAOLO
######################################################

from ..models import db, MyModel

def insertdb(iform):
    # Handle user model
    user = MyModel
    iform.populate_obj(user)
    #flash("Populated user %s" % dir(user), 'success')
    db.session.add(user)
    # Save into db
    db.session.commit()

# #@cached
@blueprint.route('/insert', methods=["GET", "POST"])
def insert():
    status = "Waiting data to save"
    iform = forms.UserForm()
    if iform.validate_on_submit():
        insertdb(iform)
        flash("User saved", 'success')
        status = "Saved"

    return render_template('forms/test.html',
        project=current_app.config['PROJECT'],
        status=status, form=iform, formname='insert')

@blueprint.route('/search', methods=["GET", "POST"])
def search():
    status = "Waiting data to search"
    iform = forms.UserForm()
    if iform.validate_on_submit():
        status = "Work in progress"
        #flash("User saved", 'success')

    return render_template('forms/test.html',
        project=current_app.config['PROJECT'],
        status=status, form=iform, formname='search')

######################################################
######################################################


################
#### basic interface routes ####
################

@blueprint.route('/')
def home():
    print(current_app.config['PROJECT'])
    return render_template('pages/placeholder.home.html',
        project=current_app.config['PROJECT'])

@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html',
        project=current_app.config['PROJECT'])

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
