#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

from flask import render_template, Blueprint, request,\
    flash, redirect, url_for
from app import forms

blueprint = Blueprint('pages', __name__)

######################################################
## PAOLO
######################################################

#Form page
@blueprint.route('/logintest', methods=["GET", "POST"])
def mylogin():
    form = forms.EmailPasswordForm()
    status = "Empty"

    if form.validate_on_submit():
        status = "Submitted"
        flash("MyModel updated", 'success')
        #return redirect(url_for('success'))
    # else:
    #     flash("Error")

    return render_template('forms/test.html', \
        form=form, status=status)

@blueprint.route('/success')
def success():
    return render_template('forms/success.html')
######################################################
######################################################


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
