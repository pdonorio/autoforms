#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" User defined model """

from ..basemodel import db, DictSerializable
# from wtforms.validators import Email, Length
# from wtforms import PasswordField
yesno = db.Enum('no', 'yes', name='yesno')


#############################################
# Work on models
class MyModel(db.Model, DictSerializable):
    """ Rizzoli's model """

    __tablename__ = 'rizzoli'

    # Primary key
    id = db.Column(db.BigInteger, autoincrement=True, primary_key=True)
    patient_id = db.Column(db.String(10))  # , unique=True)
    patient_type = db.Column(db.Enum('adult', 'child', name='age'))

    country_iso = db.Column(db.String(10))
    country = db.Column(db.String(3))
    ethnicity = db.Column(db.String(20))
    age_at_visit = db.Column(db.Integer)
    gender = db.Column(
        db.Enum('male', 'female', name='gender'))

    height_cm = db.Column(db.Integer)
    height_percentile = db.Column(db.String(9))
    weight_kg = db.Column(db.Integer)
    weight_percentile = db.Column(db.String(9))

# MISSING ADULT
    family_history = db.Column(
        db.Enum('positive', 'negative', name='familyh'))

    inheritance = db.Column(
        db.Enum('maternal', 'paternal', 'none', name='inhe'))
    imaging_evaluation = db.Column(yesno)
    affected_skeletal_site = db.Column(db.String(10))
    simmetry = db.Column(yesno)
    bones_affeced_ocs = db.Column(db.Integer)
    ior_classification = db.Column(db.String(4))
    skeletal_deformities = db.Column(db.Integer)
    deformities_localization = db.Column(db.String(9))
    functional_limitations = db.Column(db.Integer)
    limitations_localization = db.Column(db.String(20))
    spine_problems = db.Column(yesno)
    dental_abnormalities = db.Column(yesno)

# ADULT EXTRA
    malignant_degeneration = db.Column(yesno)
    sites_affected_by_psc = db.Column(db.String(20))
    age_of_psc_onset = db.Column(db.Integer)
    psc_grade = db.Column(db.String(20))
    psc_size = db.Column(db.String(20))
    psc_treatment = db.Column(db.String(20))
# ADULT EXTRA

    recurrence = db.Column(yesno)
    other_medical_diseases = db.Column(db.String(20))
    other_genetic_diseases = db.Column(db.String(20))
    germinal_mutation = db.Column(yesno)
    gene_involved = db.Column(db.String(20))
    dna_change = db.Column(db.String(20))
    protein_change = db.Column(db.String(20))
    mutation_type = db.Column(db.String(20))
    notes = db.Column(db.String(20))
