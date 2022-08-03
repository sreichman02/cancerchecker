from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email = email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Successful Login', category= 1)
                login_user(user, remember = True)
                return(redirect(url_for('views.home')))
            else:
                flash('Password is incorrect', category= 0)                
        else:
            flash('User does not exist', category = 0)

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/feedback')
@login_required
def feedback():
    return render_template("feedback.html", user = current_user)

@auth.route('/model-info')
def model_info():
    return render_template("model-info.html", user = current_user)

@auth.route('/about')
def about():
    return render_template("about.html", user = current_user)

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email = email).first()
                #category 0 for fail, 1 for success
        if user:
            flash('email already exists', category = 0)
        elif len(email) < 4:
            flash('email must be greater than four characters', category = 0)
        elif len(first_name) < 2:
            flash('Name must be greater than 2 characters', category = 0)
        elif password1 != password2:
            flash('Passwords must be the same', category = 0)
        elif len(password1) < 7:
            flash('Passwords must be greater than 7 characters', category = 0)
        else:
            new_user = User(email = email, first_name = first_name, password = generate_password_hash(password1, method = 'sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember = True)
            flash('Account Created!', category = 1)
            return(redirect(url_for('views.home')))

    return render_template("sign-up.html", user = current_user)