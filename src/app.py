"""CLI app with OOP principles."""

import argparse
import logging
import sys
from abc import ABC, abstractmethod
from typing import Any

from .pipeline_orchestrator import PipelineOrchestrator


class BaseApp(ABC):  # Abstraction
    """Abstract app (Abstraction, Encapsulation)."""
    
    def __init__(self):
        self._parser = self._create_parser()  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod  # Abstraction
    def _create_parser(self) -> argparse.ArgumentParser:
        pass
    
    def _get_mode(self) -> int:  # Encapsulation
        print("\n📋 USB Power Delivery Specification Parser")
        print("=" * 50)
        print("1. Full Document Processing")
        print("2. First 600 Pages Processing")
        print("3. First 200 Pages Processing (Memory-Safe)")
        print("=" * 50)
        while True:
            try:
                choice = int(input("Select processing mode (1-3): "))
                if choice in [1, 2, 3]:
                    return choice
            except (ValueError, KeyboardInterrupt):
                self._logger.info("Operation cancelled by user")
                sys.exit(0)


class CLIApp(BaseApp):  # Inheritance
    """CLI app (Inheritance, Polymorphism)."""
    
    def _create_parser(self) -> argparse.ArgumentParser:  # Polymorphism
        parser = argparse.ArgumentParser(
            description="USB PD Specification Parser"
        )
        parser.add_argument("--config", default="application.yml")
        parser.add_argument("--debug", action="store_true")
        parser.add_argument("--mode", type=int, choices=[1, 2, 3])
        parser.add_argument("--toc-only", action="store_true")
        parser.add_argument("--content-only", action="store_true")
        return parser
    
    def _process_args(self, args: Any) -> PipelineOrchestrator:
        """Process command line arguments (Encapsulation)."""
        if not args.mode and not args.toc_only and not args.content_only:
            args.mode = self._get_mode()
        return PipelineOrchestrator(args.config, args.debug)
    
    def _run_extraction(self, orchestrator: PipelineOrchestrator, 
                       args: Any) -> None:
        """Run extraction process (Encapsulation)."""
        self._logger.info("Starting extraction process...")
        
        if args.toc_only:
            entries = orchestrator.run_toc_only()
            self._logger.info("TOC Extraction Complete")
            self._logger.info(f"Total TOC entries extracted: {len(entries)}")
            print(f"\nSuccessfully completed! TOC entries: {len(entries)}")
        elif args.content_only:
            count = orchestrator.run_content_only()
            self._logger.info("Content Extraction Complete")
            self._logger.info(f"Total content items extracted: {count}")
            print(f"\n Successfully completed! Content items: {count}")
        else:
            results = orchestrator.run_full_pipeline(args.mode or 1)
            counts = results["spec_counts"]
            self._logger.info("Full Pipeline Execution Complete")
            self._logger.info(f"Pages processed: {counts['pages']}")
            self._logger.info(f"Paragraphs extracted: {counts['paragraphs']}")
            self._logger.info(f"TOC entries: {results['toc_entries']}")
            self._logger.info(f"TOC File: {results['toc_path']}")
            self._logger.info(f"Content File: {results['spec_path']}")
            self._logger.info(f"JSON Report: {results['report_path']}")
            self._logger.info(f"Excel Validation: {results['excel_path']}")
            
            print("\n Successfully completed!")
            pages = counts['pages']
            paragraphs = counts['paragraphs']
            toc = results['toc_entries']
            print(f" Pages: {pages} | Paragraphs: {paragraphs} | TOC: {toc}")
            files = [results['toc_path'], results['spec_path'], 
                    results['report_path'], results['excel_path']]
            print(f" Files: {len(files)} outputs generated")
        
        self._logger.info("Processing completed successfully!")
    
    def run(self) -> None:  # Polymorphism
        args = self._parser.parse_args()
        try:
            orchestrator = self._process_args(args)
            self._run_extraction(orchestrator, args)
        except Exception as e:
            self._logger.error(f"Error occurred: {e}")
            self._logger.info("Please check your configuration and try again.")
            print(f"\n Error: {e}")
            sys.exit(1)


def main():
    CLIApp().run()  # Polymorphism