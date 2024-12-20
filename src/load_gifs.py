import requests
from pathlib import Path
import json


gif_url_path = Path("resources/gif_urls.json")
all_endpoints_url: str = "https://nekos.best/api/v2/endpoints"
base_url: str = "https://nekos.best/api/v2/%s?amount=%d"
prompt: str = "hug"

categories: list[str] = [
"cuddle",
"hug",
"kiss",
"pat",
"poke",
"slap",
"highfive",
"bonk",
"clap"
]

all_data = {}

def write_gifs(file_path: Path, current_data: dict):
    with open(file_path, "w") as f:
        json.dump(current_data, f, indent=4)

def get_gif_urls(file_path: Path) -> dict[str, list[str]]:
    with open(file_path, "r") as f:
        return json.load(f)

def load_gifs(amount: int = 100):
    all_categories = requests.get(all_endpoints_url).json()
    for category in categories:
        if category not in all_categories.keys():
            print(f"Category {category} not found")
            continue

        resp = requests.get(base_url % (category, amount))
        data = resp.json()["results"]
        urls = {category: [gif["url"] for gif in data]}
        all_data.update(urls)

    write_gifs(gif_url_path, all_data)

if __name__ == "__main__":
    load_gifs()
