#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from models.portfolio import Portfolio
from models.equities import EquityInfo
from models.wallet import Wallet
from models.buy import Buys
from database import db
import uuid

'''
buying of stocks
'''

def buy_stocks(company_id, investor_id, type, quantity):
    #get company data
    stock_data = EquityInfo.query.filter_by(company_id = company_id).first()
    wallet_data = Wallet.query.filter_by(investor_id = investor_id).first()
    #make sure buy is no more than available in db
    if float(quantity) > stock_data.number_of_shares:
        return render_template('error.html', err='Cannot buy more than available supply')
    elif float(quantity) == stock_data.number_of_shares:
        return render_template('errors.html', err='Share purchase was not accepted, please try to buy a lower quantity of shares')
    elif stock_data.number_of_shares == 0 or stock_data.number_of_shares is None:
        return render_template('errors.html', err = 'There is no more supply of these stocks')
    else:
        share_price = float(stock_data.goal/stock_data.number_of_shares)
        #add to investor portfolio
        my_share_value = share_price * float(quantity)
        #add to databse
        receipt_id = str(uuid.uuid1())
        portfolio_data = Portfolio(share_type = type, share_quantity = quantity, value = my_share_value, investor_id = investor_id, receipt_id = receipt_id, company_id = company_id)
        db.session.add(portfolio_data)
        buying_data = Buys(share_quantity = quantity, value = my_share_value, receipt_id = receipt_id, investor_id = investor_id, company_id = portfolio_data.company_id)
        db.session.add(buying_data)
        #update investor wallet
        wallet_data.amount = wallet_data.amount - my_share_value
        #update company share count
        stock_data.number_of_shares = stock_data.number_of_shares - float(quantity)
        db.session.commit()
        return render_template('success.html', message = 'Thank you for your purchase', user_id = investor_id)
