from bcrypt import hashpw, gensalt
from flask import Blueprint, request, render_template, flash, redirect, url_for
from pimp_board import User, db
from flask_login import login_user, logout_user

auth_blueprint = Blueprint('auth_blueprint', __name__, template_folder='templates')

@auth_blueprint.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    plaintext_password = request.form['password'].encode('UTF_8')
    hashed_password = hashpw(plaintext_password, gensalt())
    user = User(
        email=request.form['email'],
        password=hashed_password,
        first_name=request.form['first_name'],
        last_name=request.form['last_name']
    )
    db.session.add(user)
    db.session.commit()
    flash('User successfully registered')
    return redirect(url_for('auth_blueprint.login'))
 
@auth_blueprint.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    email = request.form['email']
    password = request.form['password'].encode('UTF_8')
    registered_user = User.query.filter_by(email=email).first()
    if registered_user is None:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('auth_blueprint.login'))
    password_matches = hashpw(password, registered_user.password) == registered_user.password
    if not password_matches:
        flash('Username or Password is invalid', 'error')
        return redirect(url_for('auth_blueprint.login'))
    login_user(registered_user)
    flash('Logged in successfully')
    return redirect(request.args.get('next') or url_for('index'))

@auth_blueprint.route('/logout')
def logout():
    logout_user()
    flash('Successfull logout')
    return redirect(url_for('index'))
