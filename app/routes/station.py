from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models.station import Station

station_bp = Blueprint('station', __name__, url_prefix='/stations')

@station_bp.route('/')
@login_required
def list_stations():
    stations = Station.query.all()
    return render_template('stations.html', stations=stations)

@station_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_station():
    if current_user.role not in ['admin', 'manager']:
        flash("Permission denied.", "danger")
        return redirect(url_for('station.list_stations'))

    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        stock = float(request.form['current_stock'])
        price = float(request.form['price_per_liter'])

        new_station = Station(name=name, location=location, current_stock=stock, price_per_liter=price)
        db.session.add(new_station)
        db.session.commit()
        flash("Station added successfully.", "success")
        return redirect(url_for('station.list_stations'))

    return render_template('add_station.html')

@station_bp.route('/delete/<int:id>')
@login_required
def delete_station(id):
    if current_user.role != 'admin':
        flash("Only admins can delete stations.", "danger")
        return redirect(url_for('station.list_stations'))

    station = Station.query.get_or_404(id)
    db.session.delete(station)
    db.session.commit()
    flash("Station deleted.", "info")
    return redirect(url_for('station.list_stations'))
