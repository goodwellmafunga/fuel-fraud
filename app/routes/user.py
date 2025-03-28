from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash

user_bp = Blueprint('user', __name__, url_prefix='/users')

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
