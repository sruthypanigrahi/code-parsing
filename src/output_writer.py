"""Simple output writer for JSONL files."""

import json
from pathlib import Path
from typing import Any, Dict, List


class JSONLWriter:
    """Simple JSONL file writer."""
    
    def __init__(self, output_path: Path):
        self.output_path = output_path
        self.output_path.parent.mkdir(exist_ok=True)
    
    def write_entries(self, entries: List[Any]) -> None:
        """Write TOC entries to JSONL."""
        with open(self.output_path, "w", encoding="utf-8") as f:
            for entry in entries:
                if hasattr(entry, 'model_dump'):
                    # Pydantic model
                    f.write(entry.model_dump_json() + "\n")
                else:
                    # Regular dict
                    f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    
    def write_content(self, content_items: List[Dict[str, Any]]) -> None:
        """Write content items to JSONL."""
        with open(self.output_path, "w", encoding="utf-8") as f:
            for item in content_items:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")