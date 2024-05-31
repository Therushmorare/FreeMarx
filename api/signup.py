#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from models.company import Company
from models.investors import Investor
from database import db
from api.key_gen import uni_key_gen
'''
sign up functionality
'''

#company signup
def company_signup(email, password):
    #check if user exists in db
    company = Company.query.filter_by(email = email, password = password).first()
    if company:
        return render_template('errors.html', err='This company already exists')
    else:
        #add info into database
        user_id = str(uni_key_gen(email))
        add_company = Company(id = user_id, email = email, password = password)
        db.session.add(add_company)
        db.session.commit()
        return redirect(url_for('companySteps', id = add_company.id))
        

#investor signup
def investor_signup(first_name, last_name, email, password):
    #check if user exists
    investor = Investor.query.filter_by(email = email).first()
    if investor:
        return render_template('error.html', err='User with that email already exists!')
    else:
        #add to db
        user_id = str(uni_key_gen(email))
        add_investor = Investor(id = user_id, first_name = first_name, last_name = last_name, email = email, password = password)
        db.session.add(add_investor)
        db.session.commit()
        return redirect(url_for('investorProfileCreate', id = add_investor.id))