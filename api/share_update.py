#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from sqlalchemy import or_
from sqlalchemy import and_
from models.equities import EquityInfo
from database import db

'''
update equities
'''

def equity_update(company_id, eq_type, quantity, value):
    if eq_type is None or quantity is None or value is None:
        return render_template('errors.html', err='Please enter values')
    else:
        #main query
        share_update = EquityInfo.query.filter_by(company_id = company_id).first()
        #update each value
        share_update.number_of_shares = share_update.number_of_shares + float(quantity)
        share_update.goal = share_update.goal + float(value)
        db.session.commit()
        return redirect(url_for('companyDashboard', id = company_id))