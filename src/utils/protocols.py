"""Protocol interface for better abstraction."""

from pathlib import Path
from typing import Any, Protocol


class Extractable(Protocol):  # Protocol Abstraction
    """Protocol for extractable objects."""

    def extract(self) -> Any:
        """Extract data."""
        raise NotImplementedError(
            "Extractable implementations must define extract()."
        )


class Searchable(Protocol):  # Protocol Abstraction
    """Protocol for searchable objects."""

    def search(self, term: str) -> list[dict[str, Any]]:
        """Search for term."""
        raise NotImplementedError(
            "Searchable implementations must define search()."
        )


class Displayable(Protocol):  # Protocol Abstraction
    """Protocol for displayable objects."""

    def show(self, data: Any, term: str) -> None:
        """Display data."""
        raise NotImplementedError(
            "Displayable implementations must define show()."
        )


class Configurable(Protocol):  # Protocol Abstraction
    """Protocol for configurable objects."""

    @property
    def pdf_input_file(self) -> Path:
        """Get PDF input file path."""
        raise NotImplementedError(
            "Configurable objects must expose pdf_input_file."
        )

    @property
    def output_directory(self) -> Path:
        """Get output directory path."""
        raise NotImplementedError(
            "Configurable objects must expose output_directory."
        )


class Writable(Protocol):  # Protocol Abstraction
    """Protocol for writable objects."""

    def write(self, data: Any) -> None:
        """Write data."""
        raise NotImplementedError(
            "Writable implementations must define write()."
        )


class Cacheable(Protocol):  # Protocol Abstraction
    """Protocol for cacheable objects."""

    def cache_get(self, key: str) -> Any:
        """Get from cache."""
        raise NotImplementedError(
            "Cacheable implementations must define cache_get()."
        )

    def cache_set(self, key: str, value: Any) -> None:
        """Set cache value."""
        raise NotImplementedError(
            "Cacheable implementations must define cache_set()."
        )

    def cache_clear(self) -> None:
        """Clear cache."""
        raise NotImplementedError(
            "Cacheable implementations must define cache_clear()."
        )


# Concrete implementations for polymorphism
class BaseExtractable:  # Base class for extractable objects
    """Base extractable implementation."""

    def __init__(self) -> None:
        self.__extraction_count: int = 0  # Private counter
        self.__last_result: Any = None  # Private result cache

    @property
    def extraction_count(self) -> int:
        """Get extraction count."""
        return int(self.__extraction_count)

    def __increment_count(self) -> None:  # Private method
        """Increment extraction counter."""
        self.__extraction_count = self.__extraction_count + 1

    def __cache_result(self, result: Any) -> None:  # Private method
        """Cache extraction result."""
        self.__last_result = result

    def extract(self) -> Any:
        """Base extract implementation."""
        self.__increment_count()
        result = "extracted_data"
        self.__cache_result(result)
        return result


class FastExtractable(BaseExtractable):  # Inheritance + Polymorphism
    """Fast extractable implementation."""

    def extract(self) -> Any:  # Method override
        """Fast extraction."""
        result = super().extract()
        return f"fast_{result}"


class DetailedExtractable(BaseExtractable):  # Inheritance + Polymorphism
    """Detailed extractable implementation."""

    def extract(self) -> Any:  # Method override
        """Detailed extraction."""
        result = super().extract()
        return {"detailed": result, "count": self.extraction_count}
