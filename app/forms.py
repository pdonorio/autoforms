#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Factory and blueprints patterns """


##################################################
# http://flask.pocoo.org/snippets/60/
from flask.ext.wtf import Form
from wtforms.ext.sqlalchemy.orm import model_form
from .models import TestModel

MyForm = model_form(TestModel, Form)
print("TEST", MyForm)

##################################################
# http://wtforms-alchemy.readthedocs.org/en/latest/advanced.html#using-wtforms-alchemy-with-flask-wtf

from flask.ext.wtf import Form
from wtforms_alchemy import model_form_factory
# The variable db here is a SQLAlchemy object instance from
# Flask-SQLAlchemy package
from .models import db

BaseModelForm = model_form_factory(Form)

class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session

print(ModelForm)

##################################################
# https://exploreflask.com/forms.html
from flask.ext.wtf import Form
from wtforms.fields import TextField, PasswordField
from wtforms.validators import Required, Email, ValidationError

def my_length_check(form, field):
    if len(field.data) > 50:
        raise ValidationError('Field must be less than 50 characters')

class EmailPasswordForm(Form):
    email = TextField('Email', validators=[Required(), Email()])
    some = TextField('Some', validators=[Required(), my_length_check])
    password = PasswordField('Password', validators=[Required()])

##################################################
##################################################

from flask_wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import DataRequired, EqualTo, Length

class RegisterForm(Form):
    name = TextField(
        'Username', validators=[DataRequired(), Length(min=6, max=25)]
    )
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
    password = PasswordField(
        'Password', validators=[DataRequired(), Length(min=6, max=40)]
    )
    confirm = PasswordField(
        'Repeat Password',
        [DataRequired(),
        EqualTo('password', message='Passwords must match')]
    )


class LoginForm(Form):
    name = TextField('Username', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])


class ForgotForm(Form):
    email = TextField(
        'Email', validators=[DataRequired(), Length(min=6, max=40)]
    )
