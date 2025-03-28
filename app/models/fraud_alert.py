# app/models/fraud_alert.py

from app import db
from datetime import datetime

class FraudAlert(db.Model):
    __tablename__ = 'fraud_alerts'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), unique=True, nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.String(20), default='medium')  # e.g., low, medium, high

    def __repr__(self):
        return f"<FraudAlert Tx:{self.transaction_id} | {self.reason}>"
