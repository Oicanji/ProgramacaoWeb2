from flask import Blueprint
from flask import request, render_template, url_for, redirect, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

from .models import User
from app import db

auth = Blueprint('auth', __name__)

@auth.route('/login' , methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logado com sucesso!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Senha incorreta.', category='error')
        else:
            flash('Email não existe.', category='error')
    return render_template("pages/login.html", user=current_user)

@auth.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email já existe.', category='error')
        elif len(email) < 4:
            flash('Email deve ter mais de 3 caracteres.', category='error')
        elif len(first_name) < 2:
            flash('O nome deve ter mais de 1 caracter.', category='error')
        elif password1 != password2:
            flash('Senhas não conferem.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:

            new_user = User(email=email, first_name=first_name,
                            password=generate_password_hash(password1,
                                                            method='sha256'))
            db.session.add(new_user)
            db.session.commit()

            login_user(user, remember=True)

            flash('Conta criada!', category='success')
            return redirect(url_for('views.home'))

    return render_template("pages/singup.html", user=current_user)

