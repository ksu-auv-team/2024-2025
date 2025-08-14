from flask import Flask
from flask_marshmallow import Marshmallow
from .models import db
from .routes.batteries_routes import batteries_bp
from .routes.externals_routes import externals_bp
from .routes.imu_routes import imu_bp
from .routes.inputs_routes import inputs_bp
from .routes.internals_routes import internals_bp
from .routes.outputs_routes import outputs_bp
from .routes.sonar_routes import sonar_bp


ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db_manager.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    ma.init_app(app)
    app.register_blueprint(batteries_bp)
    app.register_blueprint(externals_bp)
    app.register_blueprint(imu_bp)
    app.register_blueprint(inputs_bp)
    app.register_blueprint(internals_bp)
    app.register_blueprint(outputs_bp)
    app.register_blueprint(sonar_bp)

    with app.app_context():
        db.create_all()

    return app
