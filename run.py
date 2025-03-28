import sys
import os
from flask import redirect, url_for

# Ensure the app package is in the path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from app import create_app, db
from flask_migrate import Migrate
from app.models import user, transaction, station, fraud_alert

# Create the app instance
app = create_app()
migrate = Migrate(app, db)

# Add shell context for Flask CLI
@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": user.User,
        "Transaction": transaction.Transaction,
        "Station": station.Station,
        "FraudAlert": fraud_alert.FraudAlert
    }

# Add a clean default route that redirects to the unified homepage
@app.route('/')
def index():
    return redirect(url_for('home.home_page'))

if __name__ == "__main__":
    app.run(debug=True)
