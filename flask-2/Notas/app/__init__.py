from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

__SECRET_KEY = os.getenv("SECRET_KEY")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = __SECRET_KEY

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app