from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    notes = db.relationship('Note')

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    note = db.Column(db.String(10000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())