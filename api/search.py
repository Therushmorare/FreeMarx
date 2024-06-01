#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from database import db
from models.company_basic_info import CompanyBasicInfo
from models.company_advanced_info import CompanyAdvancedInfo
from sqlalchemy import or_
from sqlalchemy import and_

'''
search for companies
'''

def search(company_name, user_id):
    if company_name is None:
        return render_template('errors.html', err='please enter something to search')
    else:
        results = CompanyBasicInfo.query.filter(or_(CompanyBasicInfo.name.like('%'+company_name+'%'))).all()
        results_two = CompanyAdvancedInfo.query.filter(or_(CompanyAdvancedInfo.sector.like('%'+company_name+'%'))).all()
        results_three = CompanyAdvancedInfo.query.filter(or_(CompanyAdvancedInfo.industry.like('%'+company_name+'%'))).all()
        return render_template('search.html', results = results, results_two = results_two, results_three = results_three, user_id = user_id)
        