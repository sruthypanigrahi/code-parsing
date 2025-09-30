"""Minimal CLI app with OOP principles."""

import argparse
import logging
import sys
from abc import ABC, abstractmethod
from .pipeline_orchestrator import PipelineOrchestrator


class BaseApp(ABC):  # Abstraction
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)  # Encapsulation
        logging.basicConfig(level=logging.INFO)
    
    @abstractmethod  # Abstraction
    def run(self) -> None:
        pass


class CLIApp(BaseApp):  # Inheritance
    def __init__(self):
        super().__init__()
        self._parser = self._create_parser()  # Encapsulation
    
    def _create_parser(self) -> argparse.ArgumentParser:  # Encapsulation
        parser = argparse.ArgumentParser(description="USB PD Parser")
        parser.add_argument("--config", default="application.yml")
        parser.add_argument("--mode", type=int, choices=[1, 2, 3])
        parser.add_argument("--toc-only", action="store_true")
        parser.add_argument("--content-only", action="store_true")
        return parser
    
    def _get_mode(self) -> int:  # Encapsulation
        print("Select: 1=Full, 2=600 pages, 3=200 pages")
        while True:
            try:
                choice = int(input("Mode (1-3): "))
                if 1 <= choice <= 3:
                    return choice
                print("Invalid choice")
            except (ValueError, KeyboardInterrupt):
                self._logger.warning("Invalid input")
                print("Invalid choice")
    
    def _execute_pipeline(self, args: argparse.Namespace) -> None:
        orchestrator = PipelineOrchestrator(args.config)
        if args.toc_only:
            result = orchestrator.run_toc_only()
            self._logger.info(f"TOC entries: {len(result)}")
        elif args.content_only:
            result = orchestrator.run_content_only()
            self._logger.info(f"Content items: {result}")
        else:
            mode = args.mode or self._get_mode()
            result = orchestrator.run_full_pipeline(mode)
            self._logger.info(
                f"Pipeline completed: {result['toc_entries']} TOC entries"
            )
    
    def run(self) -> None:  # Polymorphism
        try:
            args = self._parser.parse_args()
            self._execute_pipeline(args)
        except Exception as e:
            self._logger.error(f"App failed: {e}")
            sys.exit(1)


def main():
    CLIApp().run()  # Factory pattern + Polymorphism