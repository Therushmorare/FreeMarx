#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from models.wallet import Wallet, WalletTopUp
from database import db
import datetime

'''
Wallet topup and creation
'''

#new account
def balance_create(type, amount, investor_id):
    deposited_at = datetime.datetime.now()
    #add to database
    balance_add = Wallet(type = type, amount = amount, investor_id = investor_id, added_at = deposited_at)
    db.session.add(balance_add)
    db.session.commit()
    return redirect(url_for('investorDashboard', id = investor_id))
    
#topping up account
def top_up(account_type, amount, investor_id):
    #increase wallet
    topped_at = datetime.datetime.now()
    wallet_balance = Wallet.query.filter_by(investor_id = investor_id).first()
    wallet_balance.amount = wallet_balance.amount + amount
    topup_add = WalletTopUp(type = account_type, amount = amount, investor_id = investor_id, added_at = topped_at)
    db.session.add(topup_add)
    db.session.commit()
    return redirect(url_for('wallet', id=investor_id))
