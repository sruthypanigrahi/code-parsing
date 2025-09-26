"""Spec file builder."""

import json
import shutil
from pathlib import Path
from typing import Dict


class SpecBuilder:
    """Builds the final spec file."""

    def __init__(self, config, logger):
        self.cfg = config
        self.logger = logger

    def create_spec_file(self, spec_path: Path) -> dict[str, int]:
        """Create spec file by copying content file and return counts."""
        content_path = Path(self.cfg.output_directory) / "usb_pd_content.jsonl"

        shutil.copy2(content_path, spec_path)

        # Count items
        counts = {"paragraphs": 0, "images": 0, "tables": 0, "pages": 0}
        max_page = 0

        with open(spec_path, encoding="utf-8") as f:
            for line in f:
                item = json.loads(line)
                content_type = item.get("type", "")
                if content_type == "paragraph":
                    counts["paragraphs"] += 1
                elif content_type == "image":
                    counts["images"] += 1
                elif content_type == "table":
                    counts["tables"] += 1

                page_num = item.get("page", 0)
                max_page = max(max_page, page_num)

        counts["pages"] = max_page
        return counts
