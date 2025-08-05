from flask import Flask
from flask_marshmallow import Marshmallow
from .models import db
from .routes.inputs_routes import inputs_bp
from .routes.outputs_routes import outputs_bp
from .routes.batteries_routes import batteries_bp

ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_manager.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(inputs_bp)
    app.register_blueprint(outputs_bp)

    with app.app_context():
        db.create_all()

    return app
