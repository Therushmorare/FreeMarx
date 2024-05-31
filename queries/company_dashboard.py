#!/usr/bin/python3

"""
get company_data
"""

from database import db
from models.company import Company
from models.company_basic_info import CompanyBasicInfo
from models.company_advanced_info import CompanyAdvancedInfo
from models.equities import EquityInfo
from models.founder_info import FoundersInfo
from models.financial_reports import FinancialReports
from models.buy import Buys
from models.sell import Sells

def companies(id, db):
    result = Company.query.filter_by(id = id).all()
    return result

def company_info(id, db):
    result = CompanyBasicInfo.query.filter_by(company_id = id).all()
    return result

def company_info_two(id, db):
    result = CompanyAdvancedInfo.query.filter_by(company_id = id).all()
    return result

def equities(id, db):
    result = EquityInfo.query.filter_by(company_id = id).all()
    return result

def founders(id, db):
    result = FoundersInfo.query.filter_by(company_id = id).all()
    return result

def financials(id, db):
    result = FinancialReports.query.filter_by(company_id = id).all()
    return result

def buyers(id, db):
    result = Buys.query.filter_by(company_id = id).all()
    return result

def sellers(id, db):
    result = Sells.query.filter_by(company_id = id).all()
    return result