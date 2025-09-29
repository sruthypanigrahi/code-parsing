#!/usr/bin/env python3
"""Validate TOC JSONL output against TOCEntry schema."""

import json
import sys
from pathlib import Path
from typing import Any, Dict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import TOCEntry


class TOCValidator:
    """Validator for TOC JSONL files."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.valid_count = 0
        self.error_count = 0
        self.required_toc_fields = {"section_id", "title", "page"}

    def _validate_file_exists(self) -> bool:
        """Check if file exists."""
        if not self.file_path.exists():
            print(f"Error: File {self.file_path} not found")
            return False
        return True

    def _validate_required_fields(self, data: Dict[str, Any], line_num: int) -> bool:
        """Validate required TOC fields are present."""
        if not all(key in data for key in self.required_toc_fields):
            print(f"Line {line_num}: Missing required TOC fields")
            return False
        return True

    def _validate_line(self, line: str, line_num: int) -> bool:
        """Validate a single line against TOCEntry schema."""
        if not line.strip():
            return True

        try:
            data = json.loads(line)

            if not self._validate_required_fields(data, line_num):
                return False

            TOCEntry(**data)  # Validate against Pydantic model
            return True

        except json.JSONDecodeError as e:
            print(f"Line {line_num}: Invalid JSON - {e}")
            return False
        except Exception as e:
            print(f"Line {line_num}: Invalid TOCEntry - {e}")
            return False

    def _display_summary(self) -> None:
        """Display validation summary."""
        print(
            f"TOC validation complete: {self.valid_count} valid, {self.error_count} errors"
        )

    def validate(self) -> bool:
        """Validate the TOC JSONL file."""
        if not self._validate_file_exists():
            return False

        with open(self.file_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if self._validate_line(line, line_num):
                    self.valid_count += 1
                else:
                    self.error_count += 1

        self._display_summary()
        return self.error_count == 0


def validate_toc_jsonl(file_path: Path) -> bool:
    """Validate TOC JSONL file (backward compatibility)."""
    validator = TOCValidator(file_path)
    return validator.validate()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_toc.py <toc_jsonl_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    success = validate_toc_jsonl(file_path)
    sys.exit(0 if success else 1)
