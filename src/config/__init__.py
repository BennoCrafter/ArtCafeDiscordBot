from pathlib import Path
from yaml2dataclass import ConfigLoader
from src.config.config import Config


config_path = Path("config.yaml")
CONFIG: Config = ConfigLoader(config_class=Config).load_config(config_path)
