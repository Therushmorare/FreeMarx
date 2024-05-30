#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class EquityInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    number_of_shares = db.Column(db.Double)
    goal = db.Column(db.Double)
    company_id = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
