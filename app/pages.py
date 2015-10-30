#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" Main routes """

import os
from flask import Blueprint, current_app, \
    render_template, request, flash, redirect, url_for, send_from_directory
from werkzeug import secure_filename
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

# // TO FIX: move inside json
selected = [
    'id',
    'patient_id', #'patient_type', 'gender', 'imaging_evaluation']
    "patient_type", "country_iso", "country", "ethnicity", "age_at_visit", "gender", "height_cm", "height_percentile", "weight_kg", "weight_percentile", "imaging_evaluation", "affected_skeletal_site", "simmetry", "bones_affeced_ocs", "ior_classification", "skeletal_deformities", "deformities_localization", "functional_limitations", "limitations_localization", "spine_problems", "dental_abnormalities", "malignant_degeneration", "sites_affected_by_psc", "age_of_psc_onset", "psc_grade", "psc_size", "psc_treatment", "recurrence", "other_medical_diseases", "other_genetic_diseases", "germinal_mutation", "gene_involved", "dna_change", "protein_change", "mutation_type", "notes"
    ]
insertable = [
    #'patient_type', 'gender', 'ethnicity'
    "patient_type", "country_iso", "country", "ethnicity", "age_at_visit", "gender", "height_cm", "height_percentile", "weight_kg", "weight_percentile", "imaging_evaluation", "affected_skeletal_site", "simmetry", "bones_affeced_ocs", "ior_classification", "skeletal_deformities", "deformities_localization", "functional_limitations", "limitations_localization", "spine_problems", "dental_abnormalities", "malignant_degeneration", "sites_affected_by_psc", "age_of_psc_onset", "psc_grade", "psc_size", "psc_treatment", "recurrence", "other_medical_diseases", "other_genetic_diseases", "germinal_mutation", "gene_involved", "dna_change", "protein_change", "mutation_type", "notes"
]

MyTable = model2table(MyModel, selected)


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



@blueprint.route('/view', methods=["GET", "POST"])
@blueprint.route('/view/<int:id>', methods=["GET"])
def view(id=None):
    status = "View"
    template = 'forms/view.html'

    sort_field = request.args.get('sort', 'id')
    reverse = (request.args.get('direction', 'asc') == 'desc')

    field = getattr(MyModel, sort_field)
    if reverse:
        from sqlalchemy import desc
        field = desc(field)

    if id is not None:
        status = 'Single ' + status + \
            sort_field + ' for Record <b>#' + str(id) + '</b>'
        template = 'forms/singleview.html'
# from collections import OrderedDict
        items = [MyModel.query.filter(
            MyModel.id == id).first()._asdict()]
        uploaded = request.args.get('uploaded')
        if uploaded is not None:
            flash("Uploaded file '%s'" % uploaded, 'success')
    else:
        # SQLalchemy query (sorted)
        data = MyModel.query.order_by(field)
        items = []
        for row in data:
            pieces = row2dict(row)
            final = {}
            for key, value in pieces.items():
                if key in selected:
                    final[key] = value
            items.append(final)

    return render_template(template,
        status=status, formname='view', dbitems=items, id=id,
        table=MyTable(items, sort_by=sort_field, sort_reverse=reverse),
        **user_config['content'])

template = 'forms/insert_search.html'


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
        status=status, form=iform, formname='insert', selected=insertable,
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
        return redirect(url_for('.home'))

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


################
# UPLOADs
################

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in current_app.config['ALLOWED_EXTENSIONS']

# Only needed for separate debug

# # Route that will process the file upload
# @blueprint.route('/uploader/<int:id>', methods=['GET'])
# def uploader(id):
#     flash("Id is %d" % id)
#     return render_template('forms/upload.html', **user_config['content'])

# # Expecting a parameter containing the name of a file.
# # It will locate that file on the upload directory and show it
# @blueprint.route('/uploads/<filename>')
# def uploaded_file(filename):
#     return send_from_directory(current_app.config['UPLOAD_FOLDER'],
#                                filename)


# Route that will process the file upload
@blueprint.route('/upload/<int:id>', methods=['POST'])
def upload(id):
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Build the directory and make if if not exists
        mydir = os.path.join(
            current_app.config['UPLOAD_FOLDER'], str(id))
        if not os.path.exists(mydir):
            os.mkdir(mydir)
        abs_filepath = os.path.join(mydir, filename)
        # Move the file from the temporal folder
        file.save(abs_filepath)
        # Redirect
        # return redirect(url_for('.uploaded_file', filename=filename))
# // TO FIX:
# Change this to view of single id
        return redirect('/view/' + str(id) + '?uploaded=' + filename)

