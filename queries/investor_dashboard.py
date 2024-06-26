#!/usr/bin/python3

"""
get user_data
"""

from database import db
from models.investors import Investor
from models.company import Company
from models.company_basic_info import CompanyBasicInfo
from models.company_advanced_info import CompanyAdvancedInfo
from models.wallet import Wallet,WalletTopUp
from models.volume import Volume
from models.portfolio import Portfolio
from models.investor_profile import InvestorProfile
from models.equities import EquityInfo
from models.buy import Buys
from models.sell import Sells

def companies_i(db):
    result = Company.query.all()
    return result

def company_info_i(db):
    result = CompanyBasicInfo.query.all()
    return result

def company_info_two_i(db):
    result = CompanyAdvancedInfo.query.all()
    return result

def investor_info(id, db):
    result = Investor.query.filter_by(id = id).all()
    return result

def investor_profile_info(id, db):
    result = InvestorProfile.query.filter_by(investor_id = id).all()
    return result

def wallet_info(id, db):
    result = Wallet.query.filter_by(investor_id = id).all()
    return result

def port_data(id, db):
    result = Portfolio.query.filter_by(investor_id = id).all()
    return result

def port_data_two(db):
    result = Portfolio.query.all()
    return result

def profile(id, db):
    result = InvestorProfile.query.filter_by(investor_id = id).all()
    return result

def equities_i(db):
    result = EquityInfo.query.all()
    return result

def buys(db):
    result = Buys.query.count()
    return result

def buys_two(id, db):
    result = Buys.query.filter_by(investor_id = id).all()
    return result

def sells(db):
    result = Sells.query.count()
    return result

def investors(db):
    result = Investor.query.count()
    return result

def topupdata(id, db):
    result = WalletTopUp.query.filter_by(investor_id = id).all()
    return result