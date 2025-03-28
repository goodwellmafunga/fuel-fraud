# app/models/transaction.py

from app import db
from datetime import datetime

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    station_id = db.Column(db.Integer, db.ForeignKey('stations.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    fuel_type = db.Column(db.String(20), nullable=False)
    payment_method = db.Column(db.String(20))  # e.g., card, cash
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    is_flagged = db.Column(db.Boolean, default=False)
    is_fraudulent = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref='transactions')
    station = db.relationship('Station', backref='transactions')
    fraud_alert = db.relationship('FraudAlert', uselist=False, backref='transaction')

    def __repr__(self):
        return f"<Transaction {self.id} | {self.amount} | Flagged: {self.is_flagged}>"
