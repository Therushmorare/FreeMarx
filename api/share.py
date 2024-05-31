#!/usr/bin/python3

from models.equities import EquityInfo
from models.buy import Buys
from models.sell import Sells
from models.investors import Investor

"""
equations
"""

#calculate share value
def share_value(company_id):
    equity = EquityInfo.query.filter_by(company_id = company_id).first()
    money = equity.goal
    shares = equity.number_of_shares
    return float(money / shares)

#buyers sentiment
def buyers_sentiment(company_id):
    buys = Buys.query.filter_by(company_id = company_id).count()
    all_users = Investor.query.filter_by(company_id = company_id).count()
    return int((buys / all_users) * 100)

#sellers sentiment
def sellers_sentiment(company_id):
    sells = Sells.query.filter_by(company_id = company_id).count()
    all_users = Investor.query.filter_by(compnay_id = company_id).count()
    return int((sells / all_users) * 100)