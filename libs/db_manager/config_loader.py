# This module is responsible for loading configuration settings for the application.

import json
import os

def load_config(app_name : str) -> dict:
    """
    Load configuration settings from a JSON file for the specified application.
    
    :param app_name: Name of the application to load configuration for.
    :return: Dictionary containing configuration settings (including defaults).
    """
    # Get the project root directory (assuming this script is always inside the project)
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    app_config_path = os.path.join(project_dir, 'config', f'{app_name}_config.json')
    if not os.path.exists(app_config_path):
        raise FileNotFoundError(f"Configuration file '{app_config_path}' does not exist.")

    with open(app_config_path, 'r') as config_file:
        config = json.load(config_file)

    default_config_path = os.path.join(project_dir, 'config', 'default_config.json')
    if os.path.exists(default_config_path):
        with open(default_config_path, 'r') as default_file:
            default_config = json.load(default_file)
            config.update(default_config)

    return config
