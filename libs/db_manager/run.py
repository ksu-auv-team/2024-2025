from . import create_app
from .config_loader import load_config

app_name = "db_manager"
config = load_config(app_name)

app = create_app()
# Expose an ASGI app for Hypercorn/Uvicorn
asgi_app = app

if __name__ == "__main__":
    # Dev server (synchronous). For production and true async concurrency, use Hypercorn:
    #   hypercorn "libs.db_manager.run:asgi_app" --bind 0.0.0.0:5000
    app.run(host=config["app_ip"], port=config["app_port"], debug=True, threaded=True)
