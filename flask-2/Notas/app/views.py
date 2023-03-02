from flask import Blueprint
from flask import render_template
from flask_login import login_required, current_user
from flask import request, render_template, url_for, redirect, flash
from app import db
from .models import Note

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Nota está vazia.', category='error')
        else:
            new_note = Note(note=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Nota adicionada!', category='success')

    return render_template("pages/home.html", user=current_user)
