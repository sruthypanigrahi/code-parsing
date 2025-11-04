"""USB PD Specification Parser - Report Management Module"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from src.config.config import Config
from src.config.constants import USB_PD_SPEC_FILE, USB_PD_TOC_FILE
from src.core.analyzer.content_analyzer import ContentAnalyzer
from src.core.orchestrator.component import PipelineComponent
from src.support.metadata_generator import create_metadata_file
from src.support.report.report_generator import BaseReportGenerator, ReportFactory
from src.support.validation_generator import ValidationReportService

ReportGeneratorFactory = Callable[[str, Path], BaseReportGenerator]
MetadataCreator = Callable[[Path, Path], Path]
ValidationServiceFactory = Callable[[Path], ValidationReportService]
AnalyzerFactory = Callable[[], ContentAnalyzer]


class ReportManager(PipelineComponent):
    """Coordinate analysis, validation, and metadata generation for artifacts."""

    def __init__(
        self,
        config: Config,
        logger: Any,
        *,
        report_factory: ReportGeneratorFactory | None = None,
        metadata_creator: MetadataCreator | None = None,
        validation_service_factory: ValidationServiceFactory | None = None,
        analyzer_factory: AnalyzerFactory | None = None,
    ):
        """Initialize the manager with injectable collaborators."""
        super().__init__(config, logger)
        self._report_factory = report_factory or ReportFactory.create_generator
        self._metadata_creator = metadata_creator or create_metadata_file
        def _default_validation_factory(output_dir: Path) -> ValidationReportService:
            return ValidationReportService(output_dir)
        self._validation_service_factory = (
            validation_service_factory or _default_validation_factory
        )
        self._analyzer_factory = analyzer_factory or ContentAnalyzer

    def __calculate_counts(self, toc: list[Any], content: list[Any]) -> dict[str, Any]:
        """Calculate summary statistics used by downstream reports."""
        if not toc or not content:
            raise ValueError("TOC and content cannot be empty")

        analyzer = self._analyzer_factory()
        major_sections = sum(
            1 for item in content
            if analyzer.is_major_section(item.get("content", ""))
        )

        return {
            "pages": len({item.get("page", 0) for item in content}),
            "content_items": len(content),
            "toc_entries": len(toc),
            "major_sections": major_sections,
            "key_terms": 0,
            "paragraphs": sum(
                1 for item in content if item.get("type") == "paragraph"
            ),
        }

    def __create_analysis_reports(self, counts: dict[str, Any]) -> None:
        """Create JSON and Excel analysis reports."""
        output_dir = self.config.output_directory
        json_gen = self._report_factory("json", output_dir)
        json_gen.generate(counts)
        excel_gen = self._report_factory("excel", output_dir)
        excel_gen.generate(counts)

    def __create_validation_report(self) -> None:
        """Create validation report using the configured validation service."""
        output_dir = self.config.output_directory
        service = self._validation_service_factory(output_dir)
        service.generate(
            output_dir / USB_PD_TOC_FILE,
            output_dir / USB_PD_SPEC_FILE,
        )

    def __create_metadata_file(self) -> None:
        """Generate metadata artifacts alongside the reports."""
        output_dir = self.config.output_directory
        spec_file = output_dir / USB_PD_SPEC_FILE
        self._metadata_creator(output_dir, spec_file)

    def generate_reports(self, toc: list[Any], content: list[Any]) -> dict[str, Any]:
        """Generate all downstream report artifacts from the extracted data."""
        self.logger.info("Generating analysis reports...")
        counts = self.__calculate_counts(toc, content)
        self.__create_analysis_reports(counts)
        self.logger.info("Analysis reports generated successfully")

        self.logger.info("Generating validation report...")
        self.__create_validation_report()
        self.logger.info("Validation report generated successfully")

        self.logger.info("Generating metadata file...")
        self.__create_metadata_file()
        self.logger.info("Metadata file generated successfully")
        return counts
