# libs/db_manager/__init__.py
import os
from flask import Flask, jsonify
from flask_marshmallow import Marshmallow
from .models import db
from .config_loader import ConfigLoader
from .routes.inputs_routes import inputs_bp
from .routes.outputs_routes import outputs_bp
# Import others if they exist: imu_bp, sonar_bp, batteries_bp, etc.

ma = Marshmallow()


def create_app(config_path=None):
    app = Flask(__name__)
    cfg_loader = ConfigLoader(config_path)
    app.config.from_mapping(cfg_loader.as_dict())

    db.init_app(app)
    ma.init_app(app)

    app.register_blueprint(inputs_bp)
    app.register_blueprint(outputs_bp)
    # app.register_blueprint(imu_bp), etc.

    @app.errorhandler(Exception)
    def handle_any_error(err):
        # Already handled more gracefully in route‐specific try/except for logic‐thrown Errors
        # But catch unexpected exceptions here to avoid leaking stack traces
        app.logger.exception("Unhandled exception")
        return (
            jsonify({"error": "Internal Server Error", "detail": str(err)}),
            500,
        )

    with app.app_context():
        db.create_all()

    return app

