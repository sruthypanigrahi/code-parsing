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
OutputSink = Callable[[str], None]


class BaseApp(ABC):
    """Base class for CLI applications that orchestrate the pipeline."""

    def __init__(
        self,
        orchestrator_factory: PipelineFactory,
        *,
        output: OutputSink | None = None,
    ) -> None:
        """Store collaborators and initialise logging."""
        self._orchestrator_factory = orchestrator_factory
        self._logger = logging.getLogger(self.__class__.__name__)
        logging.basicConfig(level=logging.INFO)
        self._output = output or print

    @property
    def logger(self) -> logging.Logger:
        """Return the logger instance for subclasses."""
        return self._logger

    @property
    def orchestrator_factory(self) -> PipelineFactory:
        """Factory that builds orchestrators for the app."""
        return self._orchestrator_factory

    @property
    def output(self) -> OutputSink:
        """Output sink used for user-facing messages."""
        return self._output

    @abstractmethod
    def run(self) -> None:
        """Execute the application."""


class CLIApp(BaseApp):
    """Concrete CLI app that runs the pipeline based on command-line options."""

    def __init__(
        self,
        orchestrator_factory: PipelineFactory | None = None,
        *,
        parser_factory: Callable[[], argparse.ArgumentParser] | None = None,
        output: OutputSink | None = None,
    ) -> None:
        factory = orchestrator_factory or PipelineOrchestrator
        super().__init__(factory, output=output)
        parser = parser_factory() if parser_factory else self._create_parser()
        self.__parser = parser

    def _create_parser(self) -> argparse.ArgumentParser:
        """Create the argument parser for CLI usage."""
        parser = argparse.ArgumentParser(description="USB PD Parser")
        parser.add_argument("--config", default="application.yml")
        parser.add_argument("--toc-only", action="store_true")
        parser.add_argument("--content-only", action="store_true")
        return parser

    def _execute_pipeline(self, args: argparse.Namespace) -> None:
        """Execute pipeline based on parsed arguments."""
        self.output("\n=== USB PD Specification Parser ===")
        self.output("Processing entire PDF document...\n")

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

    def run(self) -> None:
        """Run the CLI application."""
        try:
            args = self.__parser.parse_args()
            self._execute_pipeline(args)
        except Exception as exc:  # pragma: no cover - defensive exit path
            msg = "Application execution failed: %s"
            self.logger.error(msg, exc)
            sys.exit(1)


def main() -> None:
    """Main entry point."""
    CLIApp().run()
