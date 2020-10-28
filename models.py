# models.py
import flask_sqlalchemy
from app import db


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(120))
    who = db.Column(db.String(120))
    time = db.Column(db.String(120))
    
    def __init__(self, a, b, c):
        self.message = a
        self.who = b
        self.time = c
        
    def __repr__(self):
        return self.message, self.who, self.time

class Responses(db.Model):
    message = db.Column(db.String(120), primary_key=True)
    response = db.Column(db.String(120))
    
    def __init__(self, a, b):
        self.response = a
        self.message = b
        
    def __repr__(self):
        return self.response
        
class Authuser(db.Model):
    name = db.Column(db.String(120), primary_key=True)
    propic = db.Column(db.String(120))
    sid = db.Column(db.String(255))
    
    def __init__(self, a, b, c):
        self.name = a
        self.propic = b
        self.sid = c
        
    def __repr__(self):
        return self.name, self.propic, self.sid



