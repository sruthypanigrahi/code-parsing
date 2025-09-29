"""CLI app with OOP principles."""

import argparse
import logging
import sys
from abc import ABC, abstractmethod

from .pipeline_orchestrator import PipelineOrchestrator


class BaseApp(ABC):  # Abstraction
    """Abstract app (Abstraction, Encapsulation)."""
    
    def __init__(self):
        self._parser = self._create_parser()  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
    
    @abstractmethod  # Abstraction
    def _create_parser(self) -> argparse.ArgumentParser:
        pass


class CLIApp(BaseApp):  # Inheritance
    """CLI app (Inheritance, Polymorphism)."""
    
    def _create_parser(self) -> argparse.ArgumentParser:  # Polymorphism
        parser = argparse.ArgumentParser(description="USB PD Parser")
        parser.add_argument("--config", default="application.yml")
        parser.add_argument("--debug", action="store_true")
        parser.add_argument("--mode", type=int, choices=[1, 2, 3])
        parser.add_argument("--toc-only", action="store_true")
        parser.add_argument("--content-only", action="store_true")
        return parser
    
    def _get_mode(self) -> int:  # Encapsulation
        print("\n📋 USB Power Delivery Parser\n" + "="*40)
        print("1. Full Document\n2. First 600 Pages\n3. First 200 Pages")
        print("="*40)
        while True:
            try:
                choice = int(input("Select mode (1-3): "))
                if choice in [1, 2, 3]:
                    return choice
            except (ValueError, KeyboardInterrupt):
                sys.exit(0)
    
    def run(self) -> None:  # Polymorphism
        args = self._parser.parse_args()
        try:
            if not args.mode and not args.toc_only and not args.content_only:
                args.mode = self._get_mode()
            
            orchestrator = PipelineOrchestrator(args.config, args.debug)
            
            if args.toc_only:
                entries = orchestrator.run_toc_only()
                print(f"\nTOC entries: {len(entries)}")
            elif args.content_only:
                count = orchestrator.run_content_only()
                print(f"\nContent items: {count}")
            else:
                results = orchestrator.run_full_pipeline(args.mode or 1)
                counts = results["spec_counts"]
                print(f"\nPages: {counts['pages']} | "
                      f"Paragraphs: {counts['paragraphs']} | "
                      f"TOC: {results['toc_entries']}")
                print(f"Files: 4 outputs generated")
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)


def main():
    CLIApp().run()  # Polymorphism