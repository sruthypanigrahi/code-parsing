"""Text preprocessing and cleaning utilities."""

import re
from typing import Any, Dict, List


class TextCleaner:
    """Handles text preprocessing and cleaning with single responsibility."""

    def __init__(self):
        self.cleaning_rules = {
            "remove_extra_whitespace": True,
            "normalize_unicode": True,
            "remove_control_chars": True,
            "fix_line_breaks": True,
        }

    def clean_text(self, text: str) -> str:
        """Clean and preprocess text content."""
        if not text:
            return ""

        cleaned = text

        # Remove control characters
        if self.cleaning_rules["remove_control_chars"]:
            cleaned = self._remove_control_chars(cleaned)

        # Normalize unicode
        if self.cleaning_rules["normalize_unicode"]:
            cleaned = self._normalize_unicode(cleaned)

        # Fix line breaks
        if self.cleaning_rules["fix_line_breaks"]:
            cleaned = self._fix_line_breaks(cleaned)

        # Remove extra whitespace
        if self.cleaning_rules["remove_extra_whitespace"]:
            cleaned = self._remove_extra_whitespace(cleaned)

        return cleaned.strip()

    def clean_toc_entry(self, title: str) -> str:
        """Clean TOC entry title."""
        if not title:
            return ""

        # Remove page numbers from end
        cleaned = re.sub(r"\s+\d+\s*$", "", title)

        # Remove dots and dashes used for alignment
        cleaned = re.sub(r"\.{2,}", " ", cleaned)
        cleaned = re.sub(r"-{2,}", " ", cleaned)

        # Clean general text
        cleaned = self.clean_text(cleaned)

        return cleaned

    def clean_content_batch(
        self, content_items: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Clean multiple content items efficiently."""
        cleaned_items = []

        for item in content_items:
            if "content" in item:
                item["content"] = self.clean_text(item["content"])

            if "title" in item:
                item["title"] = self.clean_toc_entry(item["title"])

            cleaned_items.append(item)

        return cleaned_items

    def _remove_control_chars(self, text: str) -> str:
        """Remove control characters except newlines and tabs."""
        return re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)

    def _normalize_unicode(self, text: str) -> str:
        """Normalize unicode characters."""
        # Replace common unicode quotes and dashes
        replacements = {
            "\u2018": "'",
            "\u2019": "'",  # Smart quotes
            "\u201c": '"',
            "\u201d": '"',  # Smart double quotes
            "\u2013": "-",
            "\u2014": "--",  # En/em dashes
            "\u2026": "...",  # Ellipsis
        }

        for old, new in replacements.items():
            text = text.replace(old, new)

        return text

    def _fix_line_breaks(self, text: str) -> str:
        """Fix problematic line breaks."""
        # Join hyphenated words split across lines
        text = re.sub(r"-\s*\n\s*", "", text)

        # Replace multiple newlines with single newline
        text = re.sub(r"\n{3,}", "\n\n", text)

        return text

    def _remove_extra_whitespace(self, text: str) -> str:
        """Remove extra whitespace while preserving structure."""
        # Replace multiple spaces with single space
        text = re.sub(r" {2,}", " ", text)

        # Remove trailing whitespace from lines
        text = re.sub(r" +\n", "\n", text)

        return text

    def configure_cleaning(self, **rules):
        """Configure cleaning rules."""
        self.cleaning_rules.update(rules)
