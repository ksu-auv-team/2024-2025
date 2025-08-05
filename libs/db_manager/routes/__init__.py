from .inputs_routes import inputs_bp
from .outputs_routes import outputs_bp
from .batteries_routes import batteries_bp
from .externals_routes import externals_bp
from .imu_routes import imu_bp
from .sonar_routes import sonar_bp
from .internals_routes import internals_bp

def register_routes(app):
    """
    Register all routes for the application.
    """
    app.register_blueprint(inputs_bp)
    app.register_blueprint(outputs_bp)
    app.register_blueprint(batteries_bp)
    app.register_blueprint(externals_bp)
    app.register_blueprint(imu_bp)
    app.register_blueprint(sonar_bp)
    app.register_blueprint(internals_bp)