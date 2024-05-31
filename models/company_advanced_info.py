#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class CompanyAdvancedInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sector = db.Column(db.String)
    industry = db.Column(db.String)
    employees = db.Column(db.Integer)
    details = db.Column(db.String)
    company_id = db.Column(db.String)
