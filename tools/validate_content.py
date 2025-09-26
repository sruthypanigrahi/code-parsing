#!/usr/bin/env python3
"""Validate content JSONL output."""

import json
import sys
from pathlib import Path
from collections import Counter


def validate_content_jsonl(file_path: Path) -> bool:
    """Validate each line in content JSONL file."""
    if not file_path.exists():
        print(f"Error: File {file_path} not found")
        return False
    
    valid_count = 0
    error_count = 0
    content_types = Counter()
    page_range = {"min": float('inf'), "max": 0}
    
    required_fields = {"content_type", "page", "order_on_page", "doc_title"}
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            if not line.strip():
                continue
                
            try:
                data = json.loads(line)
                
                # Check required fields
                if not required_fields.issubset(data.keys()):
                    missing = required_fields - data.keys()
                    print(f"Line {line_num}: Missing required fields: {missing}")
                    error_count += 1
                    continue
                
                # Validate content type
                content_type = data.get("content_type")
                if content_type not in ["paragraph", "image", "table"]:
                    print(f"Line {line_num}: Invalid content_type: {content_type}")
                    error_count += 1
                    continue
                
                # Validate page number
                page = data.get("page", 0)
                if not isinstance(page, int) or page <= 0 or page > 1500:
                    print(f"Line {line_num}: Invalid page number: {page}")
                    error_count += 1
                    continue
                
                # Track statistics
                content_types[content_type] += 1
                page_range["min"] = min(page_range["min"], page)
                page_range["max"] = max(page_range["max"], page)
                
                valid_count += 1
                
            except json.JSONDecodeError as e:
                print(f"Line {line_num}: Invalid JSON - {e}")
                error_count += 1
            except Exception as e:
                print(f"Line {line_num}: Validation error - {e}")
                error_count += 1
    
    # Print summary
    print(f"Content validation complete: {valid_count} valid, {error_count} errors")
    if valid_count > 0:
        print(f"Content types: {dict(content_types)}")
        if page_range["min"] != float('inf'):
            print(f"Page range: {page_range['min']} - {page_range['max']}")
    
    return error_count == 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python tools/validate_content.py <content_jsonl_file>")
        sys.exit(1)
    
    file_path = Path(sys.argv[1])
    success = validate_content_jsonl(file_path)
    sys.exit(0 if success else 1)