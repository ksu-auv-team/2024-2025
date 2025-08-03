from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config_loader import ConfigLoader

db = SQLAlchemy()
config_loader = ConfigLoader()

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = config_loader.get("DB_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    from .routes import register_routes
    register_routes(app)

    return app

