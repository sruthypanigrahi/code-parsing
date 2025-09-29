"""Base classes implementing OOP principles."""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class BaseExtractor(ABC):
    """Abstract base class for extractors (Abstraction)."""
    
    def __init__(self, config: Dict[str, Any]):
        self._config = config  # Encapsulation: private attribute
    
    @abstractmethod
    def extract(self, file_path: Path) -> List[Dict[str, Any]]:
        """Abstract method for extraction (Abstraction)."""
        pass
    
    def _validate_file(self, file_path: Path) -> None:
        """Protected method for file validation (Encapsulation)."""
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")


class BaseWriter(ABC):
    """Abstract base class for writers (Abstraction)."""
    
    def __init__(self, output_path: Path):
        self._output_path = output_path  # Encapsulation
        self._output_path.parent.mkdir(exist_ok=True)
    
    @abstractmethod
    def write(self, data: Any) -> None:
        """Abstract write method (Abstraction)."""
        pass
    
    @property
    def output_path(self) -> Path:
        """Getter for output path (Encapsulation)."""
        return self._output_path


class Processor:
    """Base processor with common functionality."""
    
    def __init__(self, name: str):
        self._name = name  # Encapsulation
        self._processed_count = 0  # Encapsulation
    
    def _increment_count(self) -> None:
        """Protected method (Encapsulation)."""
        self._processed_count += 1
    
    @property
    def processed_count(self) -> int:
        """Getter for count (Encapsulation)."""
        return self._processed_count
    
    @property
    def name(self) -> str:
        """Getter for name (Encapsulation)."""
        return self._name