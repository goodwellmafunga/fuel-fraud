# app/models/user.py

from app import db
from flask_login import UserMixin
from app import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # e.g., admin, manager, attendant

    def __repr__(self):
        return f"<User {self.username}>"

# For Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def is_admin(self):
    return self.role == 'admin'

def is_manager(self):
    return self.role == 'manager'

def is_attendant(self):
    return self.role == 'attendant'


from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user_bp', __name__, url_prefix='/users')


@user_bp.route('/')
@login_required
def list_users():
    if current_user.role != 'admin':
        flash("Admins only.", "danger")
        return redirect(url_for('dashboard.index'))

    users = User.query.all()
    return render_template('users.html', users=users)

@user_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    if current_user.role != 'admin':
        flash("Admins only.", "danger")
        return redirect(url_for('user.list_users'))

    user = User.query.get_or_404(id)

    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.role = request.form['role']
        if request.form['password']:
            user.password_hash = generate_password_hash(request.form['password'])

        db.session.commit()
        flash("User updated successfully.", "success")
        return redirect(url_for('user.list_users'))

    return render_template('edit_user.html', user=user)

@user_bp.route('/delete/<int:id>')
@login_required
def delete_user(id):
    if current_user.role != 'admin':
        flash("Admins only.", "danger")
        return redirect(url_for('user.list_users'))

    user = User.query.get_or_404(id)
    if user.id == current_user.id:
        flash("You can't delete your own account.", "warning")
        return redirect(url_for('user.list_users'))

    db.session.delete(user)
    db.session.commit()
    flash("User deleted.", "info")
    return redirect(url_for('user.list_users'))

