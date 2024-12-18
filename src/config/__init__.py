from pathlib import Path

from src.config.config_loader import ConfigLoader
from src.config.models.config import Config

config_path = Path("config.yaml")
CONFIG: Config = ConfigLoader().load_config(config_path)
