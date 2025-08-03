# This module is responsible for running the database manager application.
# libs/db_manager/run.py
import os
from . import create_app

if __name__ == "__main__":
    config_path = os.getenv("DB_MANAGER_CONFIG_PATH", None)
    app = create_app(config_path)
    host = os.getenv("DB_MANAGER_HOST", "0.0.0.0")
    port = int(os.getenv("DB_MANAGER_PORT", 5001))
    debug = os.getenv("FLASK_DEBUG", "0") in ("1", "true", "True")
    app.run(host=host, port=port, debug=debug)
    app.logger.info(f"Database Manager running on {host}:{port} with debug={debug}")