# test_transaction.py

from app import create_app, db
from app.models.transaction import Transaction
from app.models.fraud_alert import FraudAlert
from app.models.user import User
from app.models.station import Station
from app.services.fraud_detector import predict_fraud
from datetime import datetime

app = create_app()
app.app_context().push()

# Get test user and station
user = User.query.filter_by(username='attendant1').first()
station = Station.query.filter_by(name="Apex Harare Fuel Station").first()

# Create a suspicious transaction (large amount)
txn = Transaction(
    user_id=user.id,
    station_id=station.id,
    amount=5000.0,  # 🔥 intentionally large to trip fraud logic
    fuel_type='diesel',
    payment_method='cash',
    timestamp=datetime.utcnow()
)

# Run AI fraud detection
is_fraud, confidence = predict_fraud(txn)
txn.is_flagged = is_fraud
txn.is_fraudulent = is_fraud

# Save transaction
db.session.add(txn)
db.session.commit()

# Save alert if needed
if is_fraud:
    alert = FraudAlert(
        transaction_id=txn.id,
        reason=f"Flagged by AI - confidence {round(confidence * 100, 2)}%",
        severity='high' if confidence > 0.8 else 'medium'
    )
    db.session.add(alert)
    db.session.commit()

print(f"✅ Transaction added (ID: {txn.id}) — Flagged: {is_fraud} — Confidence: {confidence}")
