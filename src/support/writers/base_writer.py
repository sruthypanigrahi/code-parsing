"""Abstract Base Writer Module"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, ClassVar, Protocol

from src.utils.mixins import OutputPathMixin


class WriterProtocol(Protocol):  # Protocol for polymorphism
    """Protocol for writer implementations."""

    def write(self, data: Any) -> None:
        """Write data to output."""
        ...

    def get_format(self) -> str:
        """Get format name."""
        ...


class BaseWriter(OutputPathMixin, ABC):  # Abstraction
    """Abstract writer with encapsulation and polymorphism."""

    format_name: ClassVar[str] = "base"

    def __init__(self, output_path: Path):
        """Initialize writer with output path validation."""
        super().__init__(output_path)

    @abstractmethod  # Abstraction
    def write(self, data: Any) -> None:
        """Abstract write method - must be implemented by subclasses."""

    def get_format(self) -> str:
        """Get output format name - must be implemented by subclasses."""
        if self.format_name == "base":
            raise NotImplementedError(
                f"{self.__class__.__name__} must define format_name."
            )
        return self.format_name

    def __call__(self, data: Any) -> None:  # Magic method
        """Make writer callable."""
        self.write(data)

    def __str__(self) -> str:  # Magic method
        """String representation."""
        return f"{self.__class__.__name__}({self.output_path.name})"

    def __repr__(self) -> str:  # Magic method
        """Detailed representation."""
        return f"{self.__class__.__name__}(output_path={self.output_path!r})"

    def __eq__(self, other: object) -> bool:  # Magic method
        """Compare writers by output path."""
        if not isinstance(other, BaseWriter):
            return False
        return self.output_path == other.output_path

    def __hash__(self) -> int:  # Magic method
        """Hash based on output path."""
        return hash(self.output_path)

    @property  # Encapsulation
    def file_name(self) -> str:
        """Get file name (read-only)."""
        return self.output_path.name

    def validate_data(self, data: Any) -> bool:
        """Validate data before writing."""
        return data is not None

    def get_file_size(self) -> int:
        """Get output file size if exists."""
        if self.output_path.exists():
            return self.output_path.stat().st_size
        return 0
