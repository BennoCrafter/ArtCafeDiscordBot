import os
import json

from pathlib import Path
from src import logutil

data_file = Path("data.json")

logger = logutil.init_logger(os.path.basename(__file__))


class DataHandler:
    def __init__(self, file: Path):
        self.file = file
        self.data = self.load_data()

    def load_data(self) -> dict:
        """Load data from the JSON file."""
        if not self.file.exists():
            logger.warning(f"Data file {self.file} does not exist. Creating...")
            self.file.touch()
            return {}

        with open(self.file, "r") as f:
            return json.loads(f.read())

    def save_data(self):
        """Save data to the JSON file."""
        with open(self.file, "w") as f:
            f.write(json.dumps(self.data))

    def get(self, key: str):
        """Get a value from the data."""
        return self.data.get(key)

    def set(self, key: str, value):
        """Set a value in the data."""
        self.data[key] = value
        self.save_data()

    def delete(self, key: str):
        """Delete a key from the data."""
        if key in self.data:
            del self.data[key]
            self.save_data()

    def clear(self):
        """Clear all data."""
        self.data = {}
        self.save_data()
