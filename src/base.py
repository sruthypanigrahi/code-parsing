"""Abstract base classes for USB PD Parser interfaces."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional, Protocol


class ExtractorProtocol(Protocol):
    """Protocol for PDF extractors."""

    def extract_pages(self, max_pages: Optional[int] = None) -> list[str]:
        """Extract pages from PDF."""
        ...

    def get_doc_title(self) -> str:
        """Get document title."""
        ...


class ValidatorProtocol(Protocol):
    """Protocol for validators."""

    def validate(self) -> bool:
        """Validate data and return success status."""
        ...


class SearcherProtocol(Protocol):
    """Protocol for content searchers."""

    def search(self, search_term: str) -> list[dict[str, Any]]:
        """Search for content and return matches."""
        ...

    def display_results(self, search_term: str, max_results: int = 10) -> None:
        """Display search results."""
        ...


class BaseValidator(ABC):
    """Abstract base class for validators."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.valid_count = 0
        self.error_count = 0

    @abstractmethod
    def _validate_line(self, line: str, line_num: int) -> bool:
        """Validate a single line."""
        pass

    @abstractmethod
    def _display_summary(self) -> None:
        """Display validation summary."""
        pass

    def _validate_file_exists(self) -> bool:
        """Check if file exists."""
        if not self.file_path.exists():
            print(f"Error: File {self.file_path} not found")
            return False
        return True

    def validate(self) -> bool:
        """Validate the file."""
        if not self._validate_file_exists():
            return False

        with open(self.file_path, encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                if self._validate_line(line, line_num):
                    self.valid_count += 1
                else:
                    self.error_count += 1

        self._display_summary()
        return self.error_count == 0
