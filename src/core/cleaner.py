"""TextCleaner class for text normalization and cleanup."""

import re
from typing import Dict, List


class TextCleaner:
    """Normalization, regex cleanup."""

    def __init__(self):
        self.patterns = {
            "extra_spaces": re.compile(r"\s+"),
            "special_chars": re.compile(r"[^\w\s\.\,\!\?\-]"),
            "line_breaks": re.compile(r"\n+"),
        }

    def clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        if not text:
            return ""

        # Remove extra spaces
        text = self.patterns["extra_spaces"].sub(" ", text)

        # Normalize line breaks
        text = self.patterns["line_breaks"].sub("\n", text)

        # Remove special characters (keep basic punctuation)
        text = self.patterns["special_chars"].sub("", text)

        return text.strip()

    def clean_paragraphs(self, paragraphs: List[str]) -> List[str]:
        """Clean list of paragraphs."""
        return [self.clean_text(para) for para in paragraphs if para.strip()]

    def clean_toc_entries(self, toc_entries: List[Dict]) -> List[Dict]:
        """Clean TOC entries."""
        cleaned = []
        for entry in toc_entries:
            if "title" in entry:
                entry["title"] = self.clean_text(entry["title"])
                if entry["title"]:  # Only keep non-empty titles
                    cleaned.append(entry)
        return cleaned

    def normalize_content(self, data: Dict) -> Dict:
        """Normalize all content in structured data."""
        if "content" in data:
            data["content"] = self.clean_text(data["content"])

        if "paragraphs" in data:
            data["paragraphs"] = self.clean_paragraphs(data["paragraphs"])

        if "toc" in data:
            data["toc"] = self.clean_toc_entries(data["toc"])

        return data
