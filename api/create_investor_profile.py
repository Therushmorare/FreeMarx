#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from database import db
from models.investor_profile import InvestorProfile

'''
create profile
'''

def profile(file_name, bio_text, investor_id):
    #add to db
    profile_add = InvestorProfile(file = file_name, bio = bio_text, investor_id = investor_id)
    db.session.add(profile_add)
    db.session.commit()
    return redirect(url_for('balanceManagement', id = investor_id))

def investorP(file, bio, id):
    profile_add = InvestorProfile(file = file, bio = bio, investor_id = id)
    db.session.add(profile_add)
    db.session.commit()
    return redirect(url_for('balanceManagement', id = id))
