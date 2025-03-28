# app/models/station.py

from app import db

class Station(db.Model):
    __tablename__ = 'stations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(120), nullable=False)
    current_stock = db.Column(db.Float, nullable=True)  # in liters
    price_per_liter = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Station {self.name} - {self.location}>"
