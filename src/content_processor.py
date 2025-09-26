"""Content processing class for structured data extraction."""

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any, Dict


class ContentProcessor:
    """Processes and formats extracted content for output."""

    def __init__(self, doc_title: str):
        self.doc_title = doc_title

    def process_structured_content(
        self, content_iterator: Iterator[dict[str, Any]]
    ) -> Iterator[dict[str, Any]]:
        """Process structured content and format for JSONL output."""
        content_id = 1

        for item in content_iterator:
            processed_item = {
                "doc_title": self.doc_title,
                "content_id": f"C{content_id}",
                "type": item["type"],
                "content": item["content"],
                "page": item["page"],
                "block_id": item["block_id"],
                "bbox": item.get("bbox", []),
                "metadata": {
                    "extracted_at": self._get_timestamp(),
                    "content_length": len(item["content"]),
                },
            }

            content_id += 1
            yield processed_item

    def save_content(
        self, content_iterator: Iterator[dict[str, Any]], output_path: Path
    ) -> int:
        """Save processed content to JSONL file."""
        output_path.parent.mkdir(parents=True, exist_ok=True)

        count = 0
        with open(output_path, "w", encoding="utf-8") as f:
            for item in content_iterator:
                f.write(json.dumps(item, ensure_ascii=False) + "\n")
                count += 1

        return count

    def _get_timestamp(self) -> str:
        """Get current timestamp."""
        from datetime import datetime

        return datetime.now().isoformat()
