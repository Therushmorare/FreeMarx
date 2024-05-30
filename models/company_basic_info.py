#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class CompanyBasicInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    logo = db.Column(db.String)
    name = db.Column(db.String)
    company_id = db.Column(db.String)
