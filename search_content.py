#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search content in extracted JSONL files."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


def search_content(
    search_term: str, jsonl_file: str = "outputs/usb_pd_spec.jsonl"
) -> None:
    """Search for term in JSONL content."""
    file_path = Path(jsonl_file)
    if not file_path.exists():
        print(f"File not found: {jsonl_file}")
        return

    matches: List[Dict[str, Any]] = []
    with open(file_path, "r", encoding="utf-8") as f:
        for line_num, line in enumerate(f, 1):
            try:
                item: Dict[str, Any] = json.loads(line)
                content: str = item.get("content", "")
                if search_term.lower() in content.lower():
                    matches.append(
                        {
                            "line": line_num,
                            "page": item.get("page", "N/A"),
                            "type": item.get("type", "N/A"),
                            "content": (
                                content[:100] + "..." if len(content) > 100 else content
                            ),
                        }
                    )
            except json.JSONDecodeError:
                continue

    print(f"Found {len(matches)} matches for '{search_term}':")
    for match in matches[:10]:  # Show first 10 matches
        try:
            print(f"Page {match['page']} ({match['type']}): {match['content']}")
        except UnicodeEncodeError:
            print(
                f"Page {match['page']} ({match['type']}): [Content with special characters]"
            )

    if len(matches) > 10:
        print(f"... and {len(matches) - 10} more matches")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_content.py <search_term> [jsonl_file]")
        sys.exit(1)

    search_term: str = sys.argv[1]
    jsonl_file: str = sys.argv[2] if len(sys.argv) > 2 else "outputs/usb_pd_spec.jsonl"

    search_content(search_term, jsonl_file)
