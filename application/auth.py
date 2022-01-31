from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Inventory
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        # Here we do the check in order to ensure the user logging in 
        # has an account in the system.
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect("/")
            else:
                flash('Incorrect password, try again.', category='issue')
        else:
            flash('Username does not exist.', category='issue')

    return render_template("login.html", curUser=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Here we run checks to ensure the information given can be used
        # to create a new user.
        user = User.query.filter_by(username=username).first()
        if user:
            flash('User already exists.', category='issue')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='issue')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='issue')
        else:
            if username != "admin":
                new_user = User(username=username, password=generate_password_hash(
                    password1, method='sha256'))
            else:
                # we set an isAdmin filed in case we wish to have any admin
                # specific features such as the ability to download the product data
                # as a CSV file
                new_user = User(username=username, password=generate_password_hash(
                    password1, method='sha256'), isAdmin=True)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect("/")

    return render_template("sign_up.html", curUser=current_user)