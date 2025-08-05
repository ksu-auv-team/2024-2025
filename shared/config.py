import json
import os

def get_configs(name : str = "global") -> dict:
    global_config_path = os.path.join("configs", "global_config.json")
    # Debug
    print(f"Loading global configuration from {global_config_path}")
    if not os.path.exists(global_config_path):
        raise FileNotFoundError(f"Configuration file {global_config_path} does not exist.")
    with open(global_config_path, 'r') as config_file:
        configs = json.load(config_file)

    app_config_path = os.path.join("configs", f"{name}.json")
    # Debug
    print(f"Loading application-specific configuration from {app_config_path}")
    if not os.path.exists(app_config_path):
        raise FileNotFoundError(f"Configuration file {app_config_path} does not exist.")
    with open(app_config_path, 'r') as config_file:
        app_configs = json.load(config_file)

    # Merge global and app-specific configurations
    configs.update(app_configs)
    return configs