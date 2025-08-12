"""
@file __init__.py
@brief Flask application factory for the KSU AUV Data Visualizer.

This module exposes create_app which builds and configures the Flask app:
- Loads configuration via load_config(app_name)
- Registers routes and blueprints
- Serves templates and static assets

@details
Expected config keys (from merged project + global configs):
- "host": str, IP or hostname to bind (e.g., "0.0.0.0")
- "port": int, port to bind (e.g., 8080)
- "debug": bool, enable/disable Flask debug
- "dbhost": str, database API host (optional, used by /api proxy)
- "dbport": int, database API port (optional, used by /api proxy)
- "app_name": str (optional), if present overrides default app_name

@note The static folder is "statics" and templates folder is "templates".
"""

from flask import Flask
from .config_loader import load_config
from .logic import register_routes
from .data_getter import register_data_routes

DEFAULT_APP_NAME = "data_visualizer"

def create_app(app_name: str | None = None) -> Flask:
    """
    @brief Build and configure the Flask application.
    @param app_name Optional explicit application name used to load config.
    @return Configured Flask app instance.
    """
    # Resolve app_name preference
    chosen_name = app_name or DEFAULT_APP_NAME

    # Create Flask app with custom static/templates directories
    app = Flask(
        __name__,
        static_folder="statics",     # so url_for('static', filename='styles.css') works
        template_folder="templates"
    )

    # Load merged configuration
    config = load_config(chosen_name)
    # Allow config to override app_name itself if provided
    if isinstance(config.get("app_name"), str) and config["app_name"].strip():
        chosen_name = config["app_name"]

    # Attach config to app for downstream usage
    app.config["APP_NAME"] = chosen_name
    app.config["MERGED_CONFIG"] = config

    # Register page routes (index, health, etc.)
    register_routes(app)

    # Register optional data proxy routes if dbhost/dbport exist
    register_data_routes(app)

    return app
