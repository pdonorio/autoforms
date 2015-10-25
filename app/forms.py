#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Factory and blueprints patterns """

##################################################
# Security redirect back with Flask-wtf
# http://flask.pocoo.org/snippets/63/

try:    #python3
    from urllib.parse import urlparse, urljoin
except: #python2
    from urlparse import urlparse, urljoin
from flask import request, url_for, redirect
from flask.ext.wtf import Form
from wtforms import TextField, HiddenField

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

def get_redirect_target():
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return target

class RedirectForm(Form):
#class RedirectForm(Form):
    next = HiddenField()

    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        if not self.next.data:
            self.next.data = get_redirect_target() or ''

    def redirect(self, endpoint='index', **values):
        if is_safe_url(self.next.data):
            return redirect(self.next.data)
        target = get_redirect_target()
        return redirect(target or url_for(endpoint, **values))

##################################################
# https://exploreflask.com/forms.html
from flask.ext.wtf import Form
from wtforms import TextField, PasswordField
from wtforms.validators import Required, Email, ValidationError
from flask import flash

class FlaskForm(RedirectForm):

    def validate(self):
        rv = Form.validate(self)
        # flash("Validating!", 'warning')
        if not rv:
            flash("Failed", 'danger')
            return False
        return True

from wtforms_alchemy import model_form_factory
ModelForm = model_form_factory(FlaskForm)

# def my_length_check(form, field):
#     if len(field.data) > 5:
#         raise ValidationError('Field must be less than 50 characters')

# class EmailPasswordForm(FlaskForm):

#     email = TextField('Email', validators=[Required(), Email()])
#     #some = TextField('Some', validators=[Required(), my_length_check])
#     password = PasswordField('Password', validators=[Required()])

##################################################
## WHERE THE MAGIC HAPPENS
##################################################


from .models import User
class UserForm(ModelForm):
    class Meta:
        model = User

#     def validate(self):
#         rv = FlaskForm.validate(self)
# # Note:
# # Add code here to make db operations
#         return rv

print(UserForm)


##################################################
# ORIGINALS
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

# class LoginForm(RedirectForm):
#     name = TextField('Username', [DataRequired()])
#     password = PasswordField('Password', [DataRequired()])

class ForgotForm(Form):
    email = TextField('Email', validators=[DataRequired(), Length(min=6,max=40)])

##################################################
## YET TO TEST?
##################################################

# #http://flask.pocoo.org/snippets/64/
# from flask.ext.wtf import Form
# from wtforms import StringField, PasswordField, validators
# from .models import MyModel as User

# class LoginForm(Form):
#     username = StringField('Username', [validators.Required()])
#     password = PasswordField('Password', [validators.Required()])

#     def __init__(self, *args, **kwargs):
#         Form.__init__(self, *args, **kwargs)
#         self.user = None

#     def validate(self):
#         rv = Form.validate(self)
#         if not rv:
#             return False

#         user = User.query.filter_by(
#             username=self.username.data).first()
#         if user is None:
#             self.username.errors.append('Unknown username')
#             return False

#         if not user.check_password(self.password.data):
#             self.password.errors.append('Invalid password')
#             return False

#         self.user = user
#         return True
