from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
def home():
    # get user name to display on the page
    user = current_user

    return render_template("pages/home.html", user=user)
