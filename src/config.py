import os
from pathlib import Path
import configparser

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        self.config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent / "resources" / "config.properties"
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_path}")
        self.config.read(config_path)

    @staticmethod
    def get_property(key):
        return Config().config["DEFAULT"].get(key)

if __name__ == "__main__":
    print(Config.get_property("host"))