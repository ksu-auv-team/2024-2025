"""
@file data_getter.py
@brief Optional proxy routes for fetching DB data through the visualizer.

@details
If your UI needs to fetch data from a separate DB API (e.g., Flask service on dbhost:dbport),
this module provides a pass-through proxy at /api/<table> and /api/<table>/<id> to avoid CORS
complexities in browsers.

Expected config keys:
- "dbhost": str
- "dbport": int

Disable/remove this file or routes if you don't want proxying.
"""

from flask import Blueprint, current_app, jsonify, request, Flask
import requests

bp_data = Blueprint("data", __name__, url_prefix="/api")

def _db_base() -> str | None:
    """
    @brief Build the upstream DB API base URL from config.
    @return Base URL (e.g., "http://localhost:5000") or None if not configured.
    """
    cfg = current_app.config.get("MERGED_CONFIG", {})
    host = cfg.get("dbhost")
    port = cfg.get("dbport")
    if not host or not port:
        return None
    return f"http://{host}:{port}"

@bp_data.get("/<string:table>")
def proxy_list(table: str):
    """
    @brief Proxy GET list for a table (e.g., /api/inputs).
    @param table Table name to fetch.
    @return JSON forward from upstream DB API.
    """
    base = _db_base()
    if not base:
        return jsonify({"error": "DB upstream not configured (dbhost/dbport missing)."}), 501

    upstream_url = f"{base}/{table}"
    try:
        resp = requests.get(upstream_url, params=request.args, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except Exception as exc:
        return jsonify({"error": str(exc), "upstream": upstream_url}), 502

@bp_data.get("/<string:table>/<int:item_id>")
def proxy_get(table: str, item_id: int):
    """
    @brief Proxy GET detail for a table row (e.g., /api/inputs/123).
    @param table Table name.
    @param item_id Row ID.
    @return JSON forward from upstream DB API.
    """
    base = _db_base()
    if not base:
        return jsonify({"error": "DB upstream not configured (dbhost/dbport missing)."}), 501

    upstream_url = f"{base}/{table}/{item_id}"
    try:
        resp = requests.get(upstream_url, timeout=10)
        return jsonify(resp.json()), resp.status_code
    except Exception as exc:
        return jsonify({"error": str(exc), "upstream": upstream_url}), 502

def register_data_routes(app: Flask) -> None:
    """
    @brief Conditionally register the data proxy routes.
    @param app Flask application instance.
    """
    cfg = app.config.get("MERGED_CONFIG", {})
    if cfg.get("dbhost") and cfg.get("dbport"):
        app.register_blueprint(bp_data)
