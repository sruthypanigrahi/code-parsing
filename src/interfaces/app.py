"""Minimal CLI app with OOP principles."""

from __future__ import annotations

import argparse
import logging
import sys
from abc import ABC, abstractmethod
from typing import Callable

from src.core.orchestrator.interfaces import PipelineInterface
from src.core.orchestrator.pipeline_orchestrator import PipelineOrchestrator

PipelineFactory = Callable[[str], PipelineInterface]


class BaseApp(ABC):  # Abstraction
    def __init__(self, orchestrator_factory: PipelineFactory) -> None:
        """Initialize base application."""
        self._orchestrator_factory = orchestrator_factory
        self._logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)

    @property
    def logger(self) -> logging.Logger:
        """Get logger instance."""
        return self._logger

    @property
    def orchestrator_factory(self) -> PipelineFactory:
        """Factory that builds orchestrators for the app."""
        return self._orchestrator_factory

    @abstractmethod  # Abstraction
    def run(self) -> None:
        """Execute the application."""


class CLIApp(BaseApp):  # Inheritance
    def __init__(
        self,
        orchestrator_factory: PipelineFactory | None = None,
        parser_factory: Callable[[], argparse.ArgumentParser] | None = None,
    ) -> None:
        """Initialize CLI application."""
        factory = orchestrator_factory or PipelineOrchestrator
        super().__init__(factory)
        self.__parser = parser_factory() if parser_factory else self.__create_parser()

    def __create_parser(
        self,
    ) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(description="USB PD Parser")
        parser.add_argument("--config", default="application.yml")
        parser.add_argument("--toc-only", action="store_true")
        parser.add_argument("--content-only", action="store_true")
        return parser

    def __execute_pipeline(self, args: argparse.Namespace) -> None:
        """Execute pipeline based on arguments."""
        print("\n=== USB PD Specification Parser ===")
        print("Processing entire PDF document...\n")

        orchestrator = self.orchestrator_factory(args.config)
        if args.toc_only:
            result = orchestrator.run_toc_only()
            count = len(result)
            msg = "TOC extraction completed: %s entries"
            self.logger.info(msg, count)
        elif args.content_only:
            result = orchestrator.run_content_only()
            msg = "Content extraction completed: %s items processed"
            self.logger.info(msg, result)
        else:
            result = orchestrator.run_full_pipeline()
            toc_count = result["toc_entries"]
            content_count = result["spec_counts"]["content_items"]
            msg = "Processing completed: %s TOC entries, %s content items"
            self.logger.info(msg, toc_count, content_count)

    def run(self) -> None:  # Polymorphism
        """Run CLI application."""
        try:
            args = self.__parser.parse_args()
            self.__execute_pipeline(args)
        except Exception as e:
            msg = "Application execution failed: %s"
            self.logger.error(msg, e)
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    CLIApp().run()  # Factory pattern + Polymorphism
