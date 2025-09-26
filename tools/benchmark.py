#!/usr/bin/env python3
"""Benchmark tool for USB PD Parser performance."""

import sys
import time
from pathlib import Path
from typing import Dict, Any


def _safe_path(user_path: str) -> Path:
    """Validate path to prevent traversal attacks."""
    path = Path(user_path).resolve()
    cwd = Path.cwd().resolve()
    try:
        path.relative_to(cwd)
        return path
    except ValueError:
        raise ValueError(f"Path traversal detected: {user_path}")


# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.app import USBPDParser


def benchmark_parse(pdf_path: str) -> Dict[str, Any]:
    """Benchmark parsing performance."""
    config: Dict[str, Any] = {
        "pdf_input_file": pdf_path,
        "output": {
            "toc_file": "outputs/benchmark.jsonl",
            "output_directory": "outputs",
        },
        "extraction": {"max_pages": 10, "ocr_fallback": False},
    }

    start_time = time.time()
    parser = USBPDParser.from_dict(config)
    entries = parser.run()
    end_time = time.time()

    return {
        "parse_time": end_time - start_time,
        "entries_found": len(entries),
        "pages_processed": 10,
    }


def main():
    """Main function to run benchmark."""
    if len(sys.argv) < 2:
        print("Usage: python benchmark.py <pdf_file>")
        sys.exit(1)

    # Handle Windows command line parsing issues
    if len(sys.argv) > 2:
        pdf_path = " ".join(sys.argv[1:]).strip('"')
    else:
        pdf_path = sys.argv[1].strip('"')

    try:
        safe_path = _safe_path(pdf_path)
        if not safe_path.exists():
            print(f"PDF file not found: {pdf_path}")
            sys.exit(1)
    except ValueError as e:
        print(f"Invalid path: {e}")
        sys.exit(1)

    print(f"Benchmarking: {safe_path}")
    try:
        results = benchmark_parse(str(safe_path))

        print(f"Parse time: {results['parse_time']:.2f}s")
        print(f"Entries found: {results['entries_found']}")
        print(f"Pages processed: {results['pages_processed']}")
        parse_time = max(results["parse_time"], 0.001)  # Prevent division by zero
        print(f"Speed: {results['pages_processed']/parse_time:.1f} pages/sec")
    except Exception as e:
        print(f"Benchmark failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
