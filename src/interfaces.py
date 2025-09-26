"""Interface definitions for better modularity."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from pathlib import Path
from typing import Protocol

from .models import TOCEntry


class PDFExtractor(Protocol):
    """Protocol for PDF extraction."""

    def extract_pages(self, pdf_path: Path, max_pages: int) -> Iterator[str]:
        """Extract text from PDF pages."""
        ...

    def get_title(self, pdf_path: Path) -> str:
        """Get document title."""
        ...


class TOCParser(Protocol):
    """Protocol for TOC parsing."""

    def find_toc_lines(self, pages: Iterator[str]) -> Iterator[str]:
        """Find potential TOC lines."""
        ...

    def parse_lines(self, lines: Iterator[str]) -> Iterator[TOCEntry]:
        """Parse TOC entries from lines."""
        ...


class EntryValidator(Protocol):
    """Protocol for entry validation."""

    def validate(self, entries: Iterator[TOCEntry]) -> Iterator[TOCEntry]:
        """Validate and filter entries."""
        ...


class OutputWriter(Protocol):
    """Protocol for output writing."""

    def write(self, entries: Iterator[TOCEntry], output_path: Path) -> None:
        """Write entries to output."""
        ...


class HierarchyAssigner(Protocol):
    """Protocol for hierarchy assignment."""

    def assign(self, entries: Iterator[TOCEntry]) -> Iterator[TOCEntry]:
        """Assign hierarchy to entries."""
        ...


class ConfigProvider(Protocol):
    """Protocol for configuration."""

    @property
    def pdf_input_file(self) -> str:
        """PDF input file path."""
        ...

    @property
    def toc_file(self) -> str:
        """TOC output file path."""
        ...

    @property
    def max_pages(self) -> int | None:
        """Maximum pages to process."""
        ...


class ParsingPipeline(ABC):
    """Abstract base for parsing pipelines."""

    @abstractmethod
    def execute(self) -> list[TOCEntry]:
        """Execute the parsing pipeline."""
        ...
