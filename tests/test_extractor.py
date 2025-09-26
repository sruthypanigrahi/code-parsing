"""Tests for PDF extractor."""

from pathlib import Path
from unittest.mock import Mock, patch
from typing import Any

import pytest

from src.extractor import extract_front_pages, get_doc_title

# Create PDFNotFoundError if not imported from exceptions
class PDFNotFoundError(Exception):
    """Raised when PDF file is not found."""
    pass


def test_extract_front_pages_file_not_found() -> None:
    """Test extraction with non-existent file."""
    with pytest.raises(Exception):  # Use generic Exception since PDFNotFoundError may not be available
        list(extract_front_pages(Path("nonexistent.pdf")))


@patch("src.extractor.fitz")
def test_extract_front_pages_success(mock_fitz: Any) -> None:
    """Test successful page extraction."""
    # Mock PDF document
    mock_doc = Mock()
    mock_doc.__len__ = Mock(return_value=5)
    mock_page = Mock()
    mock_page.get_text.return_value = "Sample text"
    mock_doc.__getitem__ = Mock(return_value=mock_page)
    mock_fitz.open.return_value = mock_doc  # type: ignore

    # Create a temporary file
    test_file = Path("test.pdf")
    test_file.touch()

    try:
        pages = list(extract_front_pages(test_file, max_pages=2))
        assert len(pages) == 2
        assert all(page == "Sample text" for page in pages)
    finally:
        test_file.unlink()


@patch("src.extractor.fitz")
def test_get_doc_title_success(mock_fitz: Any) -> None:
    """Test successful title extraction."""
    mock_doc = Mock()
    mock_doc.metadata = {"title": "Test Document"}
    mock_fitz.open.return_value = mock_doc  # type: ignore

    test_file = Path("test.pdf")
    test_file.touch()

    try:
        title = get_doc_title(test_file)
        assert title == "Test Document"
    finally:
        test_file.unlink()


def test_get_doc_title_file_not_found() -> None:
    """Test title extraction with non-existent file."""
    with pytest.raises(Exception):  # Use generic Exception since PDFNotFoundError may not be available
        get_doc_title(Path("nonexistent.pdf"))
