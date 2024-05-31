#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from models.investors import Investor   
from models.company import Company

'''
login functionality
'''

def login(user_email, password):
    #check if user exists in db
    company_user = Company.query.filter_by(email = user_email).first()
    investor_user = Investor.query.filter_by(email = user_email).first()
    #check company user
    if company_user:
        return redirect(url_for('companyDashboard', id = company_user.id))
    #check investor user
    elif investor_user:
        return redirect(url_for('investorDashboard', id = investor_user.id))
    else:
        return render_template('error.html', err='User with those credentials does not exist')
    
    