#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

from flask import render_template, Blueprint, request,\
    flash#, redirect, url_for
from app import forms

blueprint = Blueprint('pages', __name__)

################################
## Paolo
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from ..models import MyModel

#MyForm = model_form(MyModel, Form)

# # Validate?
# from wtforms import validators
# MyForm = model_form(MyModel, Form, \
#     field_args = { 'name' : { 'validators' : [validators.Length(max=10)] } })

#@blueprint.route("/edit<id>")
#def edit(id):
@blueprint.route("/edit")
def edit():
    print("TEST")
    MyForm = model_form(MyModel, base_class=Form)
    print(MyForm)

    flash('test')
    flash('You were successfully logged in', 'danger')

    # model = MyModel.get(id)
    # form = MyForm(request.form, model)

    # if form.validate_on_submit():
    #     form.populate_obj(model)
    #     model.put()
    #     print("MyModel updated")
    #     return redirect(url_for("index"))
    # return render_template("edit.html", form=form)

    return render_template('pages/placeholder.edit.html')

## Paolo
################################

################
#### routes ####
################



@blueprint.route('/')
def home():
    return render_template('pages/placeholder.home.html')


@blueprint.route('/about')
def about():
    return render_template('pages/placeholder.about.html')


@blueprint.route('/login')
def login():
    form = forms.LoginForm(request.form)
    return render_template('forms/login.html', form=form)


@blueprint.route('/register')
def register():
    form = forms.RegisterForm(request.form)
    return render_template('forms/register.html', form=form)


@blueprint.route('/forgot')
def forgot():
    form = forms.ForgotForm(request.form)
    return render_template('forms/forgot.html', form=form)
