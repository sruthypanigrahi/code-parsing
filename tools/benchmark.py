#!/usr/bin/env python3
"""Benchmark tool for USB PD Parser performance."""

import sys
import time
from pathlib import Path
from typing import Any, Dict

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pipeline_orchestrator import PipelineOrchestrator


class BenchmarkRunner:
    """Benchmark runner for USB PD Parser performance."""

    def __init__(self, max_pages: int = 10):
        self.max_pages = max_pages
        self.results: Dict[str, Any] = {}

    def _validate_path(self, user_path: str) -> Path:
        """Validate path to prevent traversal attacks."""
        path = Path(user_path).resolve()
        cwd = Path.cwd().resolve()
        try:
            path.relative_to(cwd)
            return path
        except ValueError:
            raise ValueError(f"Path traversal detected: {user_path}")

    def _parse_command_line(self) -> str:
        """Parse command line arguments."""
        if len(sys.argv) < 2:
            raise ValueError("Usage: python benchmark.py <pdf_file>")

        # Handle Windows command line parsing issues
        if len(sys.argv) > 2:
            return " ".join(sys.argv[1:]).strip('"')
        return sys.argv[1].strip('"')

    def benchmark_extraction(self, pdf_path: str) -> Dict[str, Any]:
        """Benchmark extraction performance."""
        start_time = time.time()

        orchestrator = PipelineOrchestrator()
        results = orchestrator.run_full_pipeline(mode=3)  # Use memory-safe mode

        end_time = time.time()

        return {
            "parse_time": end_time - start_time,
            "entries_found": results.get("toc_entries", 0),
            "content_items": results.get("content_items", 0),
            "pages_processed": self.max_pages,
        }

    def display_results(self, results: Dict[str, Any]) -> None:
        """Display benchmark results."""
        print(f"Parse time: {results['parse_time']:.2f}s")
        print(f"TOC entries found: {results['entries_found']}")
        print(f"Content items: {results['content_items']}")
        print(f"Pages processed: {results['pages_processed']}")

        parse_time = max(results["parse_time"], 0.001)  # Prevent division by zero
        print(f"Speed: {results['pages_processed']/parse_time:.1f} pages/sec")

    def run(self) -> None:
        """Run the benchmark."""
        try:
            pdf_path = self._parse_command_line()
            safe_path = self._validate_path(pdf_path)

            if not safe_path.exists():
                raise FileNotFoundError(f"PDF file not found: {pdf_path}")

            print(f"Benchmarking: {safe_path}")
            results = self.benchmark_extraction(str(safe_path))
            self.display_results(results)

        except (ValueError, FileNotFoundError) as e:
            print(f"Error: {e}")
            sys.exit(1)
        except Exception as e:
            print(f"Benchmark failed: {e}")
            sys.exit(1)


def main() -> None:
    """Main function to run benchmark."""
    runner = BenchmarkRunner()
    runner.run()


if __name__ == "__main__":
    main()
