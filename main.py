#!/usr/bin/env python3
"""CLI entry point for USB PD Specification Parser."""

import sys
import argparse
from src.pipeline_orchestrator import PipelineOrchestrator

def main():
    parser = argparse.ArgumentParser(description="USB PD Specification Parser")
    parser.add_argument("--config", default="application.yml", help="Configuration file")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--toc-only", action="store_true", help="Extract only TOC entries")
    parser.add_argument("--content-only", action="store_true", help="Extract only content")
    parser.add_argument("--mode", type=int, choices=[1, 2, 3], 
                       help="Extraction mode: 1=All pages, 2=600 batches, 3=200 batches")
    
    args = parser.parse_args()
    
    # Interactive mode selection if not provided
    if not args.mode and not args.toc_only and not args.content_only:
        print("\nChoose extraction mode:")
        print("1. Full pipeline - Extract all pages with TOC and content (recommended)")
        print("2. Extract in 600-page batches (balanced)")
        print("3. Extract in 200-page batches (memory-safe)")
        
        while True:
            try:
                choice = int(input("\nEnter your choice (1, 2, or 3): "))
                if choice in [1, 2, 3]:
                    args.mode = choice
                    break
                else:
                    print("Please enter 1, 2, or 3")
            except ValueError:
                print("Please enter a valid number")
    
    try:
        orchestrator = PipelineOrchestrator(args.config, args.debug)
        
        if args.toc_only:
            entries = orchestrator.run_toc_only()
            print(f"\nExtracted {len(entries)} TOC entries")
        elif args.content_only:
            count = orchestrator.run_content_only()
            print(f"\nExtracted {count} content items")
        else:
            results = orchestrator.run_full_pipeline(mode=args.mode or 1)
            counts = results['spec_counts']
            print(f"\nExtraction completed successfully!")
            print(f"Total pages extracted: {counts['pages']}")
            print(f"Paragraphs: {counts['paragraphs']}")
            print(f"Images: {counts['images']}")
            print(f"Tables: {counts['tables']}")
            print(f"TOC entries: {results['toc_entries']}")
            print(f"Files created:")
            print(f"  - TOC: {results['toc_path']}")
            print(f"  - Content: {results['content_path']}")
            print(f"  - Spec: {results['spec_path']}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
