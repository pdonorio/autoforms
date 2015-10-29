#!/usr/bin/env python3
# -*- coding: utf-8 -*-

""" User defined model """

from ..basemodel import db
from wtforms.validators import Email, Length
from wtforms import PasswordField

#############################################
# Work on models

"""
PATIENT ID;FAMILY ID;COUNTRY (ISO CODE 3166);ETHNICITY;AGE AT VISIT;GENDER;
HEIGHT (cm);HEIGHT PERCENTILE (kg);WEIGHT;WEIGHT PERCENTILE;INHERITANCE ;
TOTAL IMAGING EVALUATION;

N. OF AFFECTED SKELETAL SITE ;SIMMETRY ;
N. OF BONES AFFECED BY OCs;IOR CLINICAL CLASSIFICATION;
N. OF SKELETAL DEFORMITIES;DEFORMITIES LOCALIZATION;
N. OF FUNCTIONAL LIMITATIONS;LIMITATIONS LOCALIZATION;
SPINE PROBLEMS;DENTAL ABNORMALITIES;MALIGNANT DEGENERATION ;
SITES AFFECTED BY PSC;AGE OF PSC ONSET;PSC GRADE ;PSC SIZE ;
PSC TREATMENT;RECURRENCE ;OTHER MEDICAL DISEASES;OTHER GENETIC DISEASES;
GERMINAL MUTATION;GENE INVOLVED;DNA CHANGE (c.);PROTEIN CHANGE (p.);
MUTATION TYPE;NOTE


"""

class MyModel(db.Model):

    # Primary key
    id = db.Column(db.String(10), primary_key=True)
    age = db.Column(db.Enum('adult', 'child', name='age'))

    country_iso = db.Column(db.String(10))
    country = db.Column(db.String(3))
    ethnicity = db.Column(db.String(20))
    age_at_visit = db.Column(db.Integer)
    gender = db.Column(db.Enum('male', 'female', name='gender'))

    height_cm = db.Column(db.Integer)
    height_percentile = db.Column(db.String(9))
    weight_kg = db.Column(db.Integer)
    weight_percentile = db.Column(db.String(9))

    imaging_evaluation = db.Column(db.String(20))
    affected_skeletal_site = db.Column(db.String(20))
    simmetry = db.Column(db.String(20))
    bones_affeced_ocs = db.Column(db.String(20))
    ior_classification = db.Column(db.String(20))
    skeletal_deformities = db.Column(db.String(20))
    deformities_localization = db.Column(db.String(20))
    functional_limitations = db.Column(db.String(20))
    limitations_localization = db.Column(db.String(20))
    spine_problems = db.Column(db.String(20))
    dental_abnormalities = db.Column(db.String(20))
    malignant_degeneration = db.Column(db.String(20))

    sites_affected_by_psc = db.Column(db.String(20))
    age_of_psc_onset = db.Column(db.String(20))
    psc_grade = db.Column(db.String(20))
    psc_size = db.Column(db.String(20))
    psc_treatment = db.Column(db.String(20))

    recurrence = db.Column(db.String(20))
    other_medical_diseases = db.Column(db.String(20))
    other_genetic_diseases = db.Column(db.String(20))
    germinal_mutation = db.Column(db.String(20))
    gene_involved = db.Column(db.String(20))
    dna_change = db.Column(db.String(20))
    protein_change = db.Column(db.String(20))
    mutation_type = db.Column(db.String(20))
    notes = db.Column(db.String(20))