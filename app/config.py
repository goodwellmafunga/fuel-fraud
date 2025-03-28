# app/config.py

import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or "sqlite:///fraud_system.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
