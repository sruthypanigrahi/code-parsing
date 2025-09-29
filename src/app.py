import argparse
import sys
from typing import Any, Optional

from src.input_validator import InputValidator
from src.pipeline_orchestrator import PipelineOrchestrator
from src.progress_tracker import StepTracker


class CLIInterface:
    """Command Line Interface for USB PD Parser."""

    def __init__(self):
        self.parser = self._create_parser()
        self.orchestrator: Optional[PipelineOrchestrator] = None

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(description="USB PD Specification Parser")
        parser.add_argument(
            "--config", default="application.yml", help="Configuration file"
        )
        parser.add_argument("--debug", action="store_true", help="Enable debug logging")
        parser.add_argument(
            "--toc-only", action="store_true", help="Extract only TOC entries"
        )
        parser.add_argument(
            "--content-only", action="store_true", help="Extract only content"
        )
        parser.add_argument(
            "--mode",
            type=int,
            choices=[1, 2, 3],
            help="Extraction mode: 1=All pages, 2=600 batches, 3=200 batches",
        )
        parser.add_argument(
            "--workers", type=int, default=4, help="Number of parallel workers"
        )
        return parser

    def _get_interactive_mode(self) -> int:
        """Get extraction mode through interactive prompt."""
        print("\nChoose extraction mode:")
        print("1. Full pipeline - Extract all pages with TOC and content (recommended)")
        print("2. Extract in 600-page batches (balanced)")
        print("3. Extract in 200-page batches (memory-safe)")

        while True:
            try:
                choice = int(input("\nEnter your choice (1, 2, or 3): "))
                if choice in [1, 2, 3]:
                    return choice
                print("Please enter 1, 2, or 3")
            except ValueError:
                print("Please enter a valid number")

    def _display_results(self, results: dict[str, Any]) -> None:
        """Display extraction results."""
        counts: dict[str, Any] = results["spec_counts"]
        print("\nExtraction completed successfully!")
        print(f"Total pages extracted: {counts['pages']}")
        print(f"Paragraphs: {counts['paragraphs']}")
        print(f"Images: {counts['images']}")
        print(f"Tables: {counts['tables']}")
        print(f"TOC entries: {results['toc_entries']}")
        print("Files created:")
        print(f"  - TOC: {results['toc_path']}")
        print(f"  - Spec: {results['spec_path']}")

    def run(self) -> None:
        """Run the CLI application."""
        args = self.parser.parse_args()

        # Validate configuration file if provided
        if args.config != "application.yml":
            try:
                InputValidator.validate_config_path(args.config)
            except Exception as e:
                print(f"Configuration error: {e}", file=sys.stderr)
                sys.exit(1)

        # Interactive mode selection if not provided
        if not args.mode and not args.toc_only and not args.content_only:
            args.mode = self._get_interactive_mode()

        # Set up progress tracking
        if args.toc_only:
            steps = ["Initialize", "Extract TOC", "Save Results"]
        elif args.content_only:
            steps = ["Initialize", "Extract Content", "Save Results"]
        else:
            steps = [
                "Initialize",
                "Extract TOC",
                "Extract Content",
                "Build Spec",
                "Save Results",
            ]

        tracker = StepTracker(steps, "USB PD Parser")

        try:
            tracker.next_step("Initializing pipeline...")
            self.orchestrator = PipelineOrchestrator(args.config, args.debug)

            if args.toc_only:
                tracker.next_step("Extracting TOC entries...")
                entries = self.orchestrator.run_toc_only()
                tracker.next_step("Saving results...")
                print(f"\nExtracted {len(entries)} TOC entries")
            elif args.content_only:
                tracker.next_step("Extracting content...")
                count = self.orchestrator.run_content_only()
                tracker.next_step("Saving results...")
                print(f"\nExtracted {count} content items")
            else:
                tracker.next_step("Extracting TOC...")
                tracker.next_step("Extracting content...")
                tracker.next_step("Building specification...")
                results = self.orchestrator.run_full_pipeline(mode=args.mode or 1)
                tracker.next_step("Saving results...")
                self._display_results(results)

            tracker.finish()

        except Exception as e:
            print(f"\nError: {e}", file=sys.stderr)
            sys.exit(1)
