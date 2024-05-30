#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

#host location
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String)
    building = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    country = db.Column(db.String)
    company_id = db.Column(db.String)