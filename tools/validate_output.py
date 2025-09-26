#!/usr/bin/env python3
"""Validate JSONL output against TOCEntry schema."""

import json
import sys
from pathlib import Path
from typing import Iterator

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from models import TOCEntry


def validate_jsonl(file_path: Path) -> bool:
    """Validate each line in JSONL file against TOCEntry schema."""
    if not file_path.exists():
        print(f"Error: File {file_path} not found")
        return False

    valid_count = 0
    error_count = 0

    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue

            try:
                data = json.loads(line)
                TOCEntry(**data)  # Validate against Pydantic model
                valid_count += 1
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON - {e}")
                error_count += 1
            except Exception as e:
                print(f"Line {line_num}: Invalid TOCEntry - {e}")
                error_count += 1

    print(f"Validation complete: {valid_count} valid, {error_count} errors")
    return error_count == 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_output.py <jsonl_file>")
        sys.exit(1)

    file_path = Path(sys.argv[1])
    success = validate_jsonl(file_path)
    sys.exit(0 if success else 1)
