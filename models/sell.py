#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class Sells(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    share_quantity = db.Column(db.Double)
    value = db.Column(db.Double)
    receipt_id = db.Column(db.String)
    investor_id = db.Column(db.String)
    company_id = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
