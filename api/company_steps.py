#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from database import db
from models.equities import EquityInfo
from models.company_basic_info import CompanyBasicInfo
from models.company_advanced_info import CompanyAdvancedInfo
from models.founder_info import FoundersInfo
from models.location import Location
from models.financial_reports import FinancialReports
'''
create company profile
'''

def company_profile(company_logo_file, company_name, sector, industry, employee_count, company_details, founders_doc, address, building, city, state, zip, country, equity_type, number_of_shares, financial_goal, financial_statements_doc, company_id):
    #add data to database
    basic_info = CompanyBasicInfo(company_logo = company_logo_file, company_name = company_name, company_id = company_id)
    db.session.add(basic_info)
    advanced_info = CompanyAdvancedInfo(sector = sector, industry = industry, employees = employee_count, details = company_details, company_id = company_id)
    db.session.add(advanced_info)
    founder_info = FoundersInfo(document = founders_doc, company_id = company_id)
    db.session.add(founder_info)
    location_info = Location(address = address, building = building, city = city, state = state, zip = zip, country = country, company_id = company_id)
    db.session.add(location_info)
    equity_info = EquityInfo(type = equity_type, number_of_shares = number_of_shares, goal = financial_goal, company_id = company_id)
    db.session.add(equity_info)
    financials_info = FinancialReports(document = financial_statements_doc, company_id = company_id)
    db.session.add(financials_info)
    db.session.commit()
    return redirect(url_for('companyDashboard', id = company_id))
