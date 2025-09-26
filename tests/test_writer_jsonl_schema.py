"""Test JSONL writer schema validation."""

import json
import tempfile
from pathlib import Path
from src.models import TOCEntry
from src.writer import JSONLWriter


def test_jsonl_schema_validation():
    """Test that JSONL output matches expected schema."""
    entries = [
        TOCEntry(
            doc_title="Test Doc",
            section_id="1.1",
            title="Introduction",
            page=10,
            level=2,
            full_path="1.1 Introduction",
        )
    ]

    with tempfile.NamedTemporaryFile(mode="w", suffix=".jsonl", delete=False) as f:
        temp_path = Path(f.name)

    writer = JSONLWriter()
    writer.write_list(entries, temp_path)

    # Validate each line
    with open(temp_path, "r", encoding="utf-8") as f:
        for line in f:
            data = json.loads(line.strip())
            assert "doc_title" in data
            assert "section_id" in data
            assert "title" in data
            assert "page" in data
            assert "level" in data
            assert "full_path" in data

    temp_path.unlink()
