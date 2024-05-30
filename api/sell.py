#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
import uuid
from models.sell import Sells
from models.portfolio import Portfolio
from models.equities import EquityInfo
from models.wallet import Wallet
from models.volume import Volume
from database import db
'''
selling of stocks
'''

def sell_stocks(receipt_id, investor_id, type, quantity):
    #get company data
    portfolio_data = Portfolio.filter_by(investor_id = investor_id, receipt_id = receipt_id).first()
    stock_data = EquityInfo.query.filter_by(company_id = portfolio_data.company_id, type = type).first()
    wallet_data = Wallet.query.filter_by(investor_id = investor_id).first()
    sell_id = uuid.uuid1()

    #make sure buy is no more than available in db
    if quantity > portfolio_data.share_quantity:
        return render_template('error.html', err='Cannot sell more than what you bought')
    else:
        market_price = float(stock_data.goal/stock_data.number_of_shares)
        current_price = float(portfolio_data.value/portfolio_data.share_quantity)
        if current_price < market_price:
            portfolio_data.share_quantity = portfolio_data.share_quantity - quantity
            portfolio_data.value = portfolio_data.value - market_price * quantity
            #calculate profit
            profit = (market_price * quantity) - (current_price * quantity)
            volume_data = Volume(amount = profit, type = 'profit', receipt_id = receipt_id, company_id = portfolio_data.company_id, investor_id = investor_id)
            db.session.add(volume_data)
            #add to sell db
            sells_data = Sells(share_quantity = quantity, value = market_price * quantity, sell_id = sell_id, investor_id = investor_id, company_id = portfolio_data.company_id)
            db.session.add(sells_data)
            #update wallet
            wallet_data.amount = wallet_data.amount + market_price * quantity
            db.session.commit()
            return redirect(url_for('investorDashboard', id=investor_id))
        else:
            portfolio_data.share_quantity = portfolio_data.share_quantity - quantity
            portfolio_data.value = portfolio_data.value - market_price * quantity
            #calculate profit
            loss = (market_price * quantity) - (current_price * quantity)
            volume_data = Volume(amount = loss, type = 'loss', receipt_id = receipt_id, company_id = portfolio_data.company_id, investor_id = investor_id)
            db.session.add(volume_data)
            #add to sell db
            sells_data = Sells(share_quantity = quantity, value = market_price * quantity, sell_id = sell_id, investor_id = investor_id, company_id = portfolio_data.company_id)
            db.session.add(sells_data)
            #update wallet
            wallet_data.amount = wallet_data.amount + market_price * quantity
            db.session.commit()
            return redirect(url_for('investorDashboard', id = investor_id))