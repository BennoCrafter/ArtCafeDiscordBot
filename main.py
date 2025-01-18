"""
Main script to run

This script initializes extensions and starts the bot
"""
import os
import sys

import interactions
from dotenv import load_dotenv

from pathlib import Path

from config import DEBUG, DEV_GUILD
from src.data_handler import DataHandler
from src import logutil
from src.config import CONFIG
from src.load_gifs import load_gifs
from src.translated_string import TranslatedString

TranslatedString.setup(Path("resources/translations.json"), CONFIG.language)

load_dotenv()

# Configure logging for this main.py handler
logger = logutil.init_logger()
logger.debug(
    "Debug mode is %s; This is not a warning, \
just an indicator. You may safely ignore",
    DEBUG,
)

extensions_base_path = Path("extensions")

token_type = "TOKEN" if len(sys.argv) == 1 else "DEV_TOKEN" if sys.argv[1] == "--dev" else "TOKEN"

if not os.environ.get(token_type):
    logger.critical("TOKEN variable not set. Cannot continue")
    sys.exit(1)

client = interactions.Client(
    token=os.environ.get(token_type),
    activity=interactions.Activity(
        name=str(TranslatedString("with colors")), type=interactions.ActivityType.PLAYING
    ),
    intents=interactions.Intents.ALL,
    debug_scope=DEV_GUILD,
)


@client.listen()
async def on_startup():
    logger.info(f"Logged in as {client.user.display_name}")


def get_all_extensions(for_path: Path) -> list[Path]:
    """Get all extensions Paths"""
    paths: list[Path] = []

    for path in for_path.iterdir():
        if path.is_dir() and path.stem not in ["__pycache__"]:
            paths += get_all_extensions(path)
            continue

        if path.suffix != ".py" or path.name.startswith("_"):
            continue

        paths.append(path)
    return paths

def load_extensions(extensions: list[str]):
    for extension in extensions:
        try:
            client.load_extension(extension)
            logger.info(f"Loaded extension {extension}")
        except interactions.errors.ExtensionLoadException as e:
            logger.exception(f"Failed to load extension {extension}.", exc_info=e)

def setup():
    gifs_url: Path = Path("resources/gif_urls.json")
    if gifs_url.exists():
        return

    logger.info("Beginning to load gifs")
    load_gifs(gifs_url)
    logger.info("Finished loading gifs")

if __name__ == "__main__":

    setup()
    data_handler = DataHandler.instance(Path("data.json"), default_template_file=Path("resources/data_template.json"))

    load_extensions([f"{".".join(path.parent.parts)}.{path.stem}" for path in get_all_extensions(extensions_base_path)])
    client.start()
