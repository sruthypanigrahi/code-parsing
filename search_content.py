#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Search content in extracted JSONL files."""

import json
import sys
from pathlib import Path
from typing import Dict, List, Any


class ContentSearcher:
    """Search functionality for JSONL content files."""
    
    def __init__(self, jsonl_file: str = "outputs/usb_pd_spec.jsonl"):
        self.file_path = Path(jsonl_file)
        self.matches: List[Dict[str, Any]] = []
    
    def search(self, search_term: str) -> List[Dict[str, Any]]:
        """Search for term in JSONL content."""
        if not self.file_path.exists():
            raise FileNotFoundError(f"File not found: {self.file_path}")
        
        self.matches = []
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if self._process_line(line, line_num, search_term):
                    continue
        
        return self.matches
    
    def _process_line(self, line: str, line_num: int, search_term: str) -> bool:
        """Process a single line and add to matches if found."""
        try:
            item: Dict[str, Any] = json.loads(line)
            content: str = item.get("content", "")
            if search_term.lower() in content.lower():
                self.matches.append({
                    "line": line_num,
                    "page": item.get("page", "N/A"),
                    "type": item.get("type", "N/A"),
                    "content": self._truncate_content(content),
                })
            return True
        except json.JSONDecodeError:
            return True
    
    def _truncate_content(self, content: str, max_length: int = 100) -> str:
        """Truncate content to specified length."""
        return content[:max_length] + "..." if len(content) > max_length else content
    
    def display_results(self, search_term: str, max_results: int = 10) -> None:
        """Display search results."""
        print(f"Found {len(self.matches)} matches for '{search_term}':")
        
        for match in self.matches[:max_results]:
            self._print_match(match)
        
        if len(self.matches) > max_results:
            print(f"... and {len(self.matches) - max_results} more matches")
    
    def _print_match(self, match: Dict[str, Any]) -> None:
        """Print a single match result."""
        try:
            print(f"Page {match['page']} ({match['type']}): {match['content']}")
        except UnicodeEncodeError:
            print(f"Page {match['page']} ({match['type']}): [Content with special characters]")


def search_content(search_term: str, jsonl_file: str = "outputs/usb_pd_spec.jsonl") -> None:
    """Search for term in JSONL content."""
    try:
        searcher = ContentSearcher(jsonl_file)
        searcher.search(search_term)
        searcher.display_results(search_term)
    except FileNotFoundError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python search_content.py <search_term> [jsonl_file]")
        sys.exit(1)

    search_term: str = sys.argv[1]
    jsonl_file: str = sys.argv[2] if len(sys.argv) > 2 else "outputs/usb_pd_spec.jsonl"

    search_content(search_term, jsonl_file)
