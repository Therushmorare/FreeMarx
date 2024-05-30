#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class Wallet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    amount = db.Column(db.Double)
    investor_id = db.Column(db.String)
    added_at = db.Column(db.String)
    
class WalletTopUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    amount = db.Column(db.Double)
    investor_id = db.Column(db.String)
    added_at = db.Column(db.String)
