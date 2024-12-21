from pathlib import Path


from pathlib import Path
import json

class TranslatedString:
    _initialized: bool = False
    _translations: dict[str, dict[str, str]] = {}
    _current_language = "en"

    def __init__(self, text: str, *args: str | int | float):
        self.text = text
        self.args = args

    @classmethod
    def set_language(cls, lng: str) -> bool:
        if lng not in cls._translations.keys():
            return False

        cls._current_language = lng
        return True

    @classmethod
    def load_translations_from_file(cls, path: Path):
        if cls._initialized:
            return

        with open(path, "r") as f:
            data = json.load(f)
            cls._translations = data

        return

    @classmethod
    def setup(cls, file_path: Path, language: str) -> None:
        cls.load_translations_from_file(file_path)
        cls.set_language(language)

    def get_translation(self) -> str:
        trns = TranslatedString._translations.get(TranslatedString._current_language, {})
        return trns.get(self.text, self.text).format(*self.args)

    def __str__(self) -> str:
        return self.get_translation()


if __name__ == "__main__":
    t = TranslatedString("Hello, {0} {0}", "World")
    print(str(t))
