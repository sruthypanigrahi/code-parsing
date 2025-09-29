"""Output writers with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List, TextIO, Union


class BaseWriter(ABC):  # Abstraction: abstract base class
    """Abstract writer (Abstraction, Encapsulation)."""
    
    def __init__(self, output_path: Path):
        self._output_path = output_path  # Encapsulation: protected
        self._ensure_directory()
    
    def _ensure_directory(self) -> None:  # Encapsulation: protected method
        """Ensure output directory exists."""
        self._output_path.parent.mkdir(exist_ok=True)
    
    @abstractmethod  # Abstraction: must be implemented by subclasses
    def write(self, data: Any) -> None:
        """Abstract write method."""
        pass
    
    @property  # Encapsulation: controlled access
    def output_path(self) -> Path:
        """Get output path."""
        return self._output_path


class JSONLWriter(BaseWriter):  # Inheritance: extends BaseWriter
    """JSONL file writer (Inheritance, Polymorphism)."""
    
    def write(self, data: Union[List[Any], Any]) -> None:  # Polymorphism
        """Write data to JSONL file."""
        with open(self._output_path, "w", encoding="utf-8") as f:
            if isinstance(data, list):
                self._write_list(f, data)
            else:
                self._write_single(f, data)
    
    def _write_list(self, f: TextIO, data: List[Any]) -> None:  # Encapsulation: private
        """Write list of items."""
        for item in data:
            self._write_single(f, item)
    
    def _write_single(self, f: TextIO, item: Any) -> None:  # Encapsulation: private
        """Write single item."""
        if hasattr(item, 'model_dump'):
            f.write(item.model_dump_json() + "\n")
        else:
            f.write(json.dumps(item, ensure_ascii=False) + "\n")
    
    def write_entries(self, entries: List[Any]) -> None:  # Polymorphism: specific method
        """Write TOC entries."""
        self.write(entries)
    
    def write_content(self, content: List[Dict[str, Any]]) -> None:  # Polymorphism
        """Write content items."""
        self.write(content)