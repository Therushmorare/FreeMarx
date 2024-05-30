#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class FinancialReports(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    document = db.Column(db.String)
    company_id = db.Column(db.String)
