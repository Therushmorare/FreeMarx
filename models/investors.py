#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class Investor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())