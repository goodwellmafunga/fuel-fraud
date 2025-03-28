# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app(config_class=Config):
    app = Flask(__name__, template_folder="../templates")  # Explicitly set template folder

    app.config.from_object(config_class)

    # Initialize plugins
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Register Blueprints
    from app.routes.auth import auth_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.transaction import transaction_bp
    from app.routes.user import user_bp
    from app.routes.station import station_bp
    from app.routes.home import home_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(station_bp)

    return app
