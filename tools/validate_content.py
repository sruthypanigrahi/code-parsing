#!/usr/bin/env python3
"""Validate content JSONL output."""

import json
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Dict

from ..base import BaseValidator


class ContentValidator(BaseValidator):
    """Validator for content JSONL files."""

    def __init__(self, file_path: Path):
        super().__init__(file_path)
        self.content_types = Counter()
        self.page_range = {"min": float("inf"), "max": 0}
        self.required_fields = {"content_type", "page", "order_on_page", "doc_title"}
        self.valid_content_types = {"paragraph", "image", "table"}

    def _validate_file_exists(self) -> bool:
        """Check if file exists."""
        if not self.file_path.exists():
            print(f"Error: File {self.file_path} not found")
            return False
        return True

    def _validate_required_fields(self, data: Dict[str, Any], line_num: int) -> bool:
        """Validate required fields are present."""
        if not self.required_fields.issubset(data.keys()):
            missing = self.required_fields - data.keys()
            print(f"Line {line_num}: Missing required fields: {missing}")
            return False
        return True

    def _validate_content_type(self, content_type: str, line_num: int) -> bool:
        """Validate content type is valid."""
        if content_type not in self.valid_content_types:
            print(f"Line {line_num}: Invalid content_type: {content_type}")
            return False
        return True

    def _validate_page_number(self, page: Any, line_num: int) -> bool:
        """Validate page number is valid."""
        if not isinstance(page, int) or page <= 0 or page > 1500:
            print(f"Line {line_num}: Invalid page number: {page}")
            return False
        return True

    def _update_statistics(self, data: Dict[str, Any]) -> None:
        """Update validation statistics."""
        content_type = data.get("content_type")
        page = data.get("page", 0)

        self.content_types[content_type] += 1
        self.page_range["min"] = min(self.page_range["min"], page)
        self.page_range["max"] = max(self.page_range["max"], page)

    def _validate_line(self, line: str, line_num: int) -> bool:
        """Validate a single line."""
        if not line.strip():
            return True

        try:
            data = json.loads(line)

            if not self._validate_required_fields(data, line_num):
                return False

            content_type = data.get("content_type")
            if not self._validate_content_type(content_type, line_num):
                return False

            page = data.get("page", 0)
            if not self._validate_page_number(page, line_num):
                return False

            self._update_statistics(data)
            return True

        except json.JSONDecodeError as e:
            print(f"Line {line_num}: Invalid JSON - {e}")
            return False
        except Exception as e:
            print(f"Line {line_num}: Validation error - {e}")
            return False

    def _display_summary(self) -> None:
        """Display validation summary."""
        print(
            f"Content validation complete: {self.valid_count} valid, {self.error_count} errors"
        )
        if self.valid_count > 0:
            print(f"Content types: {dict(self.content_types)}")
            if self.page_range["min"] != float("inf"):
                print(
                    f"Page range: {self.page_range['min']} - {self.page_range['max']}"
                )

    # Inherits validate() method from BaseValidator


def validate_content_jsonl(file_path: Path) -> bool:
    """Validate content JSONL file (backward compatibility)."""
    validator = ContentValidator(file_path)
    return validator.validate()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_content.py <content_jsonl_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    success = validate_content_jsonl(file_path)
    sys.exit(0 if success else 1)
