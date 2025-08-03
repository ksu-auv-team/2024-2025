# libs/db_manager/config_loader.py
import os
from pathlib import Path
import yaml


class ConfigLoader:
    """
    Loads a YAML config (e.g. local_configs/db_manager.yaml),
    merges with global_config.yaml and environment vars.
    """

    def __init__(self, path=None):
        config_path = Path(path or os.getenv("DB_MANAGER_CONFIG", "config/local_configs/db_manager.yaml"))
        self._config = {}
        if config_path.exists():
            with config_path.open() as f:
                self._config = yaml.safe_load(f) or {}

        # Fall back to global_config.yaml on reuse
        global_path = Path("config/global_config.yaml")
        if global_path.exists():
            with global_path.open() as gf:
                global_cfg = yaml.safe_load(gf) or {}
            self._config = {**global_cfg.get("db_manager", {}), **self._config}

    def as_dict(self):
        return {
            "SQLALCHEMY_DATABASE_URI": self._config.get("database_uri", "sqlite:///db_manager.db"),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "JSON_SORT_KEYS": False,
            **self._config.get("flask", {})
        }

    def __repr__(self):
        return f"<ConfigLoader  uri={self._config.get('database_uri')}>"
