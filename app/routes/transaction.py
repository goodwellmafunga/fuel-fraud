# app/routes/transaction.py

from flask import Blueprint, request, jsonify, render_template
from flask_login import login_required, current_user
from app import db
from app.models.transaction import Transaction
from app.models.fraud_alert import FraudAlert
from app.models.station import Station
from app.services.fraud_detector import predict_fraud

transaction_bp = Blueprint('transaction', __name__, url_prefix='/transactions')

@transaction_bp.route('/new', methods=['POST'], endpoint='submit_transaction')  # 👈 explicit endpoint
@login_required
def new_transaction():
    data = request.json
    try:
        station = Station.query.get(data['station_id'])
        if not station:
            return jsonify({"error": "Invalid station ID"}), 400

        # Create transaction
        txn = Transaction(
            user_id=current_user.id,
            station_id=station.id,
            amount=data['amount'],
            fuel_type=data['fuel_type'],
            payment_method=data['payment_method'],
        )

        # Run fraud detection
        is_fraud, confidence = predict_fraud(txn)
        txn.is_flagged = is_fraud
        txn.is_fraudulent = is_fraud  # could later be manually confirmed

        db.session.add(txn)
        db.session.commit()

        # Save alert if needed
        if is_fraud:
            alert = FraudAlert(
                transaction_id=txn.id,
                reason=f"AI flagged transaction (confidence: {round(confidence * 100, 2)}%)",
                severity="high" if confidence > 0.8 else "medium"
            )
            db.session.add(alert)
            db.session.commit()

        return jsonify({"message": "Transaction processed", "flagged": is_fraud}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@transaction_bp.route('/history')
@login_required
def transaction_history():
    txns = Transaction.query.order_by(Transaction.timestamp.desc()).all()
    return render_template('transaction_history.html', transactions=txns)
