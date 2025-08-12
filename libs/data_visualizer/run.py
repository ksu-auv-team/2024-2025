"""
@file run.py
@brief Entry point to run the Flask development server.

@details
Reads host/port/debug from merged config via the app factory. Use this for local
development or simple deployment. For production, prefer a WSGI server (gunicorn, uwsgi).
"""

from . import create_app

if __name__ == "__main__":
    app = create_app()

    # cfg = app.config.get("MERGED_CONFIG", {})
    # host = cfg.get("host", "0.0.0.0")
    # port = int(cfg.get("port", 5002))
    # debug = bool(cfg.get("debug", False))

    # Note: threaded=True is handy for simple streaming fetches/refreshes
    app.run(host="0.0.0.0", port=5002, debug=True, threaded=True)
