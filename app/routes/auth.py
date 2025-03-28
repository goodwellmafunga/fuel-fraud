# app/routes/auth.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app.models.user import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard.index'))  # adjust to your landing page
        else:
            flash('Invalid username or password.', 'danger')

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


from werkzeug.security import generate_password_hash

@auth_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    if current_user.role != 'admin':
        flash("Only admins can register new users.", "danger")
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        password = request.form['password']

        existing = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing:
            flash("Username or email already exists.", "danger")
            return redirect(url_for('auth.register'))

        new_user = User(
            username=username,
            email=email,
            role=role,
            password_hash=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()
        flash(f"User '{username}' registered successfully.", "success")
        return redirect(url_for('auth.register'))

    return render_template('register.html')
