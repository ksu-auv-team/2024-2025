"""
@file logic.py
@brief Page routes and simple helpers for the visualizer.

@details
Defines the main UI routes:
- GET / : renders the index.html template
- GET /healthz : liveness probe
- GET /config.json : exposes a tiny subset of config to the frontend (optional)

All styling and behavior is handled via templates/index.html and statics/*.
"""

from flask import Blueprint, current_app, jsonify, render_template, Flask

bp = Blueprint("ui", __name__)

@bp.get("/")
def index():
    """
    @brief Render the main UI.
    @return Rendered HTML template for the single-page app.
    """
    return render_template("index.html")

@bp.get("/healthz")
def healthz():
    """
    @brief Simple liveness endpoint.
    @return JSON with status ok.
    """
    return jsonify({"status": "ok"}), 200

@bp.get("/config.json")
def front_config():
    """
    @brief Expose minimal frontend configuration (optional).
    @details Only includes values that are safe/necessary for the client.
    @return JSON subset of configuration.
    """
    cfg = current_app.config.get("MERGED_CONFIG", {})
    public_cfg = {
        "appName": current_app.config.get("APP_NAME", "data_visualizer"),
        "dbHost": cfg.get("dbhost"),
        "dbPort": cfg.get("dbport"),
        "cameraBaseUrl": cfg.get("camera_base_url", "http://localhost:5001"),
    }
    return jsonify(public_cfg), 200

def register_routes(app: Flask) -> None:
    """
    @brief Register the UI blueprint with the Flask app.
    @param app Flask application instance.
    """
    app.register_blueprint(bp)
