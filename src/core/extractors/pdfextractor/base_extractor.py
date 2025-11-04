"""Base PDF extractor modules."""

import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class BaseExtractor(ABC):  # Abstraction
    """Abstract PDF extractor (Abstraction, Encapsulation)."""

    def __init__(self, pdf_path: Path) -> None:
        self.__pdf_path = pdf_path  # Private encapsulation
        class_name = self.__class__.__name__
        self.__logger = logging.getLogger(class_name)  # Private
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF not found: {pdf_path}")

    @property
    def pdf_path(self) -> Path:
        """Public read-only PDF path."""
        return self.__pdf_path

    @property
    def pdf_name(self) -> str:
        """Public read-only PDF name."""
        return self.__pdf_path.name

    @property
    def logger(self) -> Any:
        """Public read-only logger access."""
        return self.__logger

    @abstractmethod  # Abstraction
    def extract(self) -> Any:
        """Extract content from PDF."""
        raise NotImplementedError(
            f"{self.__class__.__name__}.extract() must be implemented by subclasses."
        )

    def _get_fitz(self) -> Any:  # Encapsulation
        """Get fitz module."""
        import fitz

        return fitz


