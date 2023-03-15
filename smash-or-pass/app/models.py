from . import db
from flask_login import UserMixin
from .base.user import User

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=db.func.now())
    create_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    allow_allias = db.Column(db.String(100))
    super_allow_allias = db.Column(db.String(100))
    deny_allias = db.Column(db.String(100))
    allow_color = db.Column(db.String(7))
    deny_color = db.Column(db.String(7))
    allow_color_super = db.Column(db.String(7))
    list_answers = db.relationship('Answers')
    list_categories = db.relationship('ListCategories')

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    image = db.Column(db.String(500))
    attribute = db.Column(db.String(20000))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))

class Categories(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    categories_id = db.Column(db.Integer, db.ForeignKey('categories.id'))

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    color = db.Column(db.String(100))

class ListAnswers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_quiz = db.Column(db.Integer, db.ForeignKey('quiz.id'))
    answers = db.relationship('Answers')

"""
ANSWERS - Resolução dos questionários
É responsa
"""
class Answers(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'))
    id_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    list_answers = db.relationship('Answer')

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_question = db.Column(db.Integer, db.ForeignKey('question.id'))
    value = db.Column(db.String(100))

class User(db.Model, UserMixin, User):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    first_name = db.Column(db.String(100))
    type = db.Column(db.String(100))
