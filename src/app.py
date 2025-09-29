#!/usr/bin/env python3
"""Simple CLI for USB PD Parser"""

import argparse
import sys
from pathlib import Path

from .pipeline_orchestrator import PipelineOrchestrator


def get_mode_choice():
    """Get extraction mode interactively."""
    print("\nChoose extraction mode:")
    print("1. Full pipeline - Extract all pages (recommended)")
    print("2. Extract first 600 pages (balanced)")
    print("3. Extract first 200 pages (memory-safe)")
    
    while True:
        try:
            choice = int(input("\nEnter choice (1, 2, or 3): "))
            if choice in [1, 2, 3]:
                return choice
            print("Please enter 1, 2, or 3")
        except (ValueError, KeyboardInterrupt):
            print("\nExiting...")
            sys.exit(0)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="USB PD Specification Parser")
    parser.add_argument("--config", default="application.yml", help="Config file")
    parser.add_argument("--debug", action="store_true", help="Debug logging")
    parser.add_argument("--mode", type=int, choices=[1, 2, 3], help="Extraction mode")
    parser.add_argument("--toc-only", action="store_true", help="Extract only TOC")
    parser.add_argument("--content-only", action="store_true", help="Extract only content")
    
    args = parser.parse_args()
    
    try:
        # Get mode if not specified
        if not args.mode and not args.toc_only and not args.content_only:
            args.mode = get_mode_choice()
        
        # Initialize orchestrator
        orchestrator = PipelineOrchestrator(args.config, args.debug)
        
        # Run extraction
        if args.toc_only:
            print("Extracting TOC only...")
            entries = orchestrator.run_toc_only()
            print(f"Extracted {len(entries)} TOC entries")
        elif args.content_only:
            print("Extracting content only...")
            count = orchestrator.run_content_only()
            print(f"Extracted {count} content items")
        else:
            print(f"Running full extraction (mode {args.mode})...")
            results = orchestrator.run_full_pipeline(mode=args.mode or 1)
            
            # Display results
            counts = results["spec_counts"]
            print(f"\nExtraction completed!")
            print(f"Pages: {counts['pages']}")
            print(f"Paragraphs: {counts['paragraphs']}")
            print(f"Images: {counts['images']}")
            print(f"Tables: {counts['tables']}")
            print(f"TOC entries: {results['toc_entries']}")
            print(f"Files: {results['toc_path']}, {results['spec_path']}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()