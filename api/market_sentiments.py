#!/usr/bin/python3

from flask import Flask, render_template, redirect, url_for
from sqlalchemy.sql import func

'''
market sentiment
'''

#get the data from db
buyers = Buys.query.count()
sellers = Sells.query.count()
investors = Investors.query.count()

def buyer_sentiment():
    return int((buyers / investors) * 100)

def sell_sentiment():
    return int((sellers / investors) *100)
