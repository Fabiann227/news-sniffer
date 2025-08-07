import re
import json
import os

class TextCleaner:
    def __init__(self, config_path="cleaner/regex.json"):
        self.title_patterns = []
        self.content_patterns = []
        self.load_patterns(config_path)

    def load_patterns(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            config = json.load(f)
            self.title_patterns = config.get("title_cleaning_patterns", [])
            self.content_patterns = config.get("content_cleaning_patterns", [])

    def clean_title(self, title: str) -> str:
        for pattern in self.title_patterns:
            title = re.sub(pattern, '', title, flags=re.IGNORECASE)
        return title.strip()

    def clean_content(self, content: str) -> str:
        for pattern in self.content_patterns:
            content = re.sub(pattern, '', content, flags=re.IGNORECASE | re.MULTILINE)
        return content.strip()
