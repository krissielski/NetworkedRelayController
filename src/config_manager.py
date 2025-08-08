import yaml
import os
from typing import Any, Dict

class ConfigManager:
    def __init__(self, config_path: str):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"Config file not found: {self.config_path}")
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
        self._validate_config(config)
        return config

    def _validate_config(self, config: Dict[str, Any]):
        # Basic validation for required keys
        required = ['api', 'relays', 'logging', 'system']
        for key in required:
            if key not in config:
                raise ValueError(f"Missing required config section: {key}")
        if 'pins' not in config['relays']:
            raise ValueError("Missing relay pin mappings in config")

    def get(self, section: str, key: str = None):
        if section not in self.config:
            raise KeyError(f"Config section not found: {section}")
        if key:
            return self.config[section].get(key)
        return self.config[section]
