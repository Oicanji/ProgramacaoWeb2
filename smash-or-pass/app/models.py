from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    type = db.Column(db.String(100))

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    create_by = db.Column(db.Integer, db.ForeignKey('User.id'))
    categories = db.relationship('ListCategories')

class ListCategories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    categories_id = db.Column(db.Integer, db.ForeignKey('Categories.id'))

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))

class Char(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(500))
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    statistics = db.relationship('Statistics')

class Statistics(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(100))
    value = db.Column(db.Integer)

class StatisticsResult(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    char_id = db.Column(db.Integer, db.ForeignKey('Char.id'))

class CharRespost(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('Quiz.id'))
    char_id = db.Column(db.Integer, db.ForeignKey('Char.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))