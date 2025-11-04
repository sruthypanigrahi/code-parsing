"""USB PD Specification Parser - Data Extraction Module"""

from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import Any, Callable, Optional, Protocol

from src.config.config import Config
from src.core.extractors.pdfextractor.pdf_extractor import PDFExtractor
from src.core.extractors.strategies.extraction_strategy import (
    ComprehensiveStrategy,
    ExtractionStrategy,
)
from src.core.extractors.tocextractor.toc_extractor import TOCExtractor
from src.core.orchestrator.component import PipelineComponent


class ExtractionModeStrategy(Protocol):
    """Protocol describing a pipeline extraction mode."""

    name: str

    def execute(self, extractor: DataExtractor, max_pages: Optional[int]) -> Any:
        """Execute the strategy for the provided extractor."""
        ...


class FullPipelineMode:
    """Default strategy that extracts both TOC and content."""

    name = "full"

    def execute(self, extractor: DataExtractor, max_pages: Optional[int]) -> Any:
        return extractor.extract_data(max_pages)


class TocOnlyMode:
    """Strategy that extracts only the TOC."""

    name = "toc"

    def execute(self, extractor: DataExtractor, max_pages: Optional[int]) -> Any:
        _ = max_pages  # Explicitly ignore to satisfy the interface
        return extractor.extract_toc_only()


class ContentOnlyMode:
    """Strategy that extracts content only."""

    name = "content"

    def execute(self, extractor: DataExtractor, max_pages: Optional[int]) -> Any:
        _ = max_pages
        return extractor.extract_content_only()


class DataExtractor(PipelineComponent):
    """Handles all data extraction operations."""

    def __init__(
        self,
        config: Config,
        logger: Any,
        *,
        toc_extractor_factory: Callable[[], TOCExtractor] | None = None,
        content_strategy: ExtractionStrategy | None = None,
        pdf_extractor_factory: Callable[[Path], PDFExtractor] | None = None,
        modes: Iterable[ExtractionModeStrategy] | None = None,
    ) -> None:
        super().__init__(config, logger)
        self._toc_extractor_factory = toc_extractor_factory or TOCExtractor
        self._content_strategy = content_strategy or ComprehensiveStrategy()
        def _default_factory(path_arg: Path) -> PDFExtractor:
            return PDFExtractor(path_arg)
        self._pdf_extractor_factory = pdf_extractor_factory or _default_factory

        default_modes = modes or (
            FullPipelineMode(),
            TocOnlyMode(),
            ContentOnlyMode(),
        )
        self._mode_registry: dict[str, ExtractionModeStrategy] = {
            mode.name: mode for mode in default_modes
        }

    def register_mode(self, strategy: ExtractionModeStrategy) -> None:
        """Register or replace an extraction mode strategy."""
        self._mode_registry[strategy.name] = strategy

    def __extract_toc(self) -> list[Any]:
        """Extract Table of Contents."""
        self.logger.info("Extracting Table of Contents...")
        pdf_file = self.config.pdf_input_file
        toc_extractor = self._toc_extractor_factory()
        toc = toc_extractor.extract_toc(pdf_file)
        toc_count = len(toc)
        self.logger.info("TOC extraction completed: %s entries", toc_count)
        return toc

    def __extract_content(self, max_pages: Optional[int] = None) -> list[Any]:
        """Extract content using the configured strategy."""
        if max_pages is not None and max_pages < 1:
            raise ValueError("max_pages must be positive")

        pages_info = max_pages or "all"
        self.logger.info("Extracting content (max pages: %s)...", pages_info)

        pdf_file = self.config.pdf_input_file
        content = list(self._content_strategy.extract_pages(pdf_file, max_pages))
        count = len(content)
        self.logger.info("Content extraction completed: %s items", count)
        return content

    def extract_data(self, max_pages: Optional[int]) -> tuple[list[Any], list[Any]]:
        """Extract both TOC and content data."""
        toc = self.__extract_toc()
        content = self.__extract_content(max_pages)
        return toc, content

    def extract_toc_only(self) -> Any:
        """Extract TOC only for specialized operations."""
        toc_extractor = self._toc_extractor_factory()
        return toc_extractor.extract_toc(self.config.pdf_input_file)

    def extract_content_only(self) -> int:
        """Extract content only for specialized operations."""
        pdf_file = self.config.pdf_input_file
        extractor = self._pdf_extractor_factory(pdf_file)
        return len(extractor.extract_content())

    def extract(self, mode: str = "full", max_pages: Optional[int] = None) -> Any:
        """Extract data using a registered mode strategy."""
        try:
            strategy = self._mode_registry[mode]
        except KeyError as exc:
            raise ValueError(f"Unknown extraction mode: {mode}") from exc
        return strategy.execute(self, max_pages)
