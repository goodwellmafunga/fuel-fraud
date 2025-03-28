import joblib
import numpy as np
import os

# Define the model path
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../../ml_model/fraud_model.pkl")

# Try loading model
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

# Dummy fallback logic for fraud prediction
def predict_fraud(transaction):
    # If a model is successfully loaded in future, use it:
    if model:
        try:
            features = np.array([[transaction.amount]])  # Update with real features if needed
            prediction = model.predict(features)[0]
            probability = model.predict_proba(features)[0][1]
            return bool(prediction), round(probability, 2)
        except Exception as e:
            print(f"Model prediction error: {e}")
            return False, 0.0

    # Fallback dummy logic
    if transaction.amount > 1000:
        return True, 0.92
    return False, 0.05
