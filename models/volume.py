#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class Volume(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Double)
    type = db.Column(db.String)
    receipt_id = db.Column(db.String)
    company_id = db.Column(db.String)
    investor_id = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
