import os

import json
from pathlib import Path
from src.logutil import init_logger
from typing import Any, Optional, Union


logger = init_logger(os.path.basename(__file__))

class DataHandler:
    _instance = None

    @classmethod
    def instance(cls, file: Path | None = None, default_template_file: Path | None = None):
        if cls._instance is None:
            if file is None:
                raise ValueError("A file path must be provided for the initial creation.")
            cls._instance = cls(file, default_template_file)
        return cls._instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DataHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, file: Path, default_template_file: Path | None = None):
        if not hasattr(self, "initialized"):
            self.file = file
            self.data = self.load_data_from_file(default_template_file)
            self.initialized = True

    def load_data_from_file(self, default_template: Path | None):
        """Load the data from the JSON file."""
        if self.file.exists():
            with open(self.file, "r") as f:
                return json.load(f)


        if default_template is None:
            logger.warning("No default template provided.")
            return {}

        if not default_template.exists():
            logger.warning(f"Template file {default_template.absolute()} does not exist.")
            return {}

        with open(default_template, "r") as f:
            return json.load(f)

    def save_data_to_file(self):
        """Save the data to the JSON file."""
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=4)

    def import_template_to_data(self, filepath: Path):
        """Import a template into the data."""
        with open(filepath, "r") as f:
            template_data = json.load(f)

        def recursive_store(data, parent_key=""):
            for key, value in data.items():
                full_key = f"{parent_key}.{key}" if parent_key else key
                if isinstance(value, dict):
                    recursive_store(value, full_key)
                else:
                    self.set(full_key, value)

        if not template_data:
            raise ValueError("Default template is empty or not loaded.")

        recursive_store(template_data)

    def get(self, key: str, default: Optional[Any] = None) -> Any:
        """
        Get a value from the nested data structure.
        If the key doesn't exist, return the default value.
        """
        keys = key.split(".")
        data: Union[dict, Any, None] = self.data
        for k in keys:
            if not isinstance(data, dict):
                return default
            data = data.get(k, None)

        return data if data is not None else default

    def set(self, key: str, value):
        """Set a value in the data."""
        keys = key.split(".")
        data = self.data
        for k in keys[:-1]:
            data = data.setdefault(k, {})
        data[keys[-1]] = value
        self.save_data_to_file()

    def delete(self, key: str):
        """Delete a key from the data."""
        keys = key.split(".")
        data = self.data
        for k in keys[:-1]:
            data = data.get(k, {})
        if keys[-1] in data:
            del data[keys[-1]]
        self.save_data_to_file()

    def clear(self):
        """Clear all data."""
        self.data = {}
        self.save_data_to_file()
