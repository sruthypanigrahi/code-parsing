"""USB PD Specification Parser - Pipeline Coordinator Module"""

from __future__ import annotations

import logging
from typing import Any, Callable, Optional

from src.config.config import Config
from src.core.orchestrator.base_pipeline import BasePipeline
from src.core.orchestrator.component import PipelineComponent
from src.core.orchestrator.data_extractor import DataExtractor
from src.core.orchestrator.file_manager import FileManager
from src.core.orchestrator.interfaces import PipelineInterface
from src.core.orchestrator.report_manager import ReportManager
from src.utils.decorators import log_execution, timing

DataExtractorFactory = Callable[[Config, Any], DataExtractor]
FileManagerFactory = Callable[[Config, Any], FileManager]
ReportManagerFactory = Callable[[Config, Any], ReportManager]
ConfigFactory = Callable[[str], Config]
LoggerFactory = Callable[[str], logging.Logger]


class PipelineCoordinator(PipelineComponent, BasePipeline, PipelineInterface):
    """Coordinates pipeline execution with separation of concerns."""

    def __init__(
        self,
        config_path: str,
        *,
        config_factory: ConfigFactory | None = None,
        logger_factory: LoggerFactory | None = None,
        data_extractor_factory: DataExtractorFactory | None = None,
        file_manager_factory: FileManagerFactory | None = None,
        report_manager_factory: ReportManagerFactory | None = None,
    ):
        """Initialize pipeline coordinator with configuration."""
        if not config_path:
            raise ValueError("Config path cannot be empty")

        config_factory = config_factory or Config
        logger_factory = logger_factory or logging.getLogger
        class_name = self.__class__.__name__
        logger = logger_factory(class_name)

        try:
            config = config_factory(config_path)
            logger.info("Configuration loaded from %s", config_path)
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e

        super().__init__(config, logger)

        extractor_factory = data_extractor_factory or DataExtractor
        file_factory = file_manager_factory or FileManager
        report_factory = report_manager_factory or ReportManager

        # Initialize components with dependency injection
        self.__data_extractor = extractor_factory(self.config, self.logger)
        self.__file_manager = file_factory(self.config, self.logger)
        self.__report_manager = report_factory(self.config, self.logger)

    def __get_max_pages(self) -> Optional[int]:  # Private method
        """Get max pages for processing."""
        return None  # Process all pages

    def __get_mode_name(self) -> str:  # Private method
        """Get mode name for logging."""
        return "Full Document Processing"

    @timing
    @log_execution
    def run(self) -> dict[str, Any]:  # Polymorphism
        """Execute the complete pipeline."""
        mode_name = self.__get_mode_name()
        self.logger.info("Starting pipeline execution - %s", mode_name)

        max_pages = self.__get_max_pages()
        toc, content = self.__data_extractor.extract_data(max_pages)
        self.__file_manager.write_files(toc, content)
        counts = self.__report_manager.generate_reports(toc, content)

        self.logger.info("Pipeline execution completed successfully")
        return {"toc_entries": len(toc), "spec_counts": counts}

    def run_toc_only(self) -> Any:  # Polymorphism
        """Extract TOC only."""
        return self.__data_extractor.extract_toc_only()

    def run_content_only(self) -> int:  # Polymorphism
        """Extract content only."""
        return self.__data_extractor.extract_content_only()

    def run_full_pipeline(self) -> dict[str, Any]:
        """Run full pipeline - Polymorphism."""
        return self.run()
