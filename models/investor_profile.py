#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class InvestorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file = db.Column(db.String)
    bio = db.Column(db.String)
    investor_id = db.Column(db.String)
