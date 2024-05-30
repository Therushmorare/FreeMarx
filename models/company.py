#!/usr/bin/python3

from database import db
from sqlalchemy.sql import func

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    password = db.Column(db.String)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())