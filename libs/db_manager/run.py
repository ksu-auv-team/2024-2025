from . import create_app
from .config_loader import load_config

app_name = "db_manager"
config = load_config(app_name)

app = create_app()

if __name__ == "__main__":
    app.run(host=config["app_ip"], port=config["app_port"], debug=True)
