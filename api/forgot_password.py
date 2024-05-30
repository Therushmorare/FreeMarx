#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from models.investors import Investor
from models.company import Company
from database import db
'''
forgot password
'''

#investor password reset
def investor_reset(email):
    #check if user exists first
    investor = Investor.query.filter_by(email = email).first()
    if not investor:
        return render_template('error.html', err='User with that email does not exist')
    else:
        return redirect(url_for('newPassword', email = email))

#reset password
def investor_new_password(password, confirm_password, email):
    if password == confirm_password:
        #add to db
        investor = Investor.query.filter_by(email = email).first()
        investor.password = password
        db.session.commit()
        return redirect(url_for('investorDashboard', id = investor.id))
    else:
        return render_template('error.html', err='Please make sure the passwords are identical')

#company password reset
def company_reset(email):
    #check if user exists first
    investor = Company.query.filter_by(email = email).first()
    if not investor:
        return render_template('error.html', err='User with that email does not exist')
    else:
        return redirect(url_for('newCompanyPassword', email = email))

#reset password
def company_new_password(password, confirm_password, email):
    if password == confirm_password:
        #add to db
        company = Company.query.filter_by(email = email).first()
        company.password = password
        db.session.commit()
        return redirect(url_for('companyDashboard', id = company.id))
    else:
        return render_template('error.html', err='Please make sure the passwords are identical')
