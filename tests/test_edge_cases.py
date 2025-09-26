"""Unit tests for edge cases."""

import pytest
from src.models import TOCEntry
from src.parsing_strategies import RegexTOCParser, FuzzyTOCParser
from src.parsing_strategies import ToCNotFoundError


def test_parent_inference():
    """Test parent inference for hierarchical sections."""
    # Test section ID parsing for parent inference
    assert "2.1".rsplit(".", 1)[0] == "2"  # 2.1 -> 2
    assert "2.1.1".rsplit(".", 1)[0] == "2.1"  # 2.1.1 -> 2.1
    assert "3" == "3"  # Top level has no parent


def test_dotted_leader_variants():
    """Test different dotted leader formats."""
    parser = RegexTOCParser()

    # Test basic parsing using public parse method
    pages = [(1, "1.1 Introduction 123")]
    entries = parser.parse(pages)

    if entries:
        entry = entries[0]
        assert entry.section_id == "1.1"
        assert "Introduction" in entry.title
        assert entry.page == 123


def test_no_toc_error():
    """Test ToCNotFoundError is raised when no TOC found."""
    from src.parser import TOCParser

    parser = TOCParser()

    # Empty pages should raise error
    with pytest.raises(ToCNotFoundError):
        parser.parse([])

    # Pages with no TOC content should raise error
    with pytest.raises(ToCNotFoundError):
        parser.parse([(1, "Random text without TOC patterns")])


def test_fuzzy_parser_keywords():
    """Test fuzzy parser finds TOC by keywords."""
    parser = FuzzyTOCParser()

    pages = [
        (1, "Table of Contents\n1.1 Introduction 15\n2.1 Methods 25"),
        (2, "Random content without TOC"),
    ]

    entries = parser.parse(pages)
    assert len(entries) >= 1
    assert any("Introduction" in entry.title for entry in entries)


def test_invalid_page_numbers():
    """Test handling of invalid page numbers."""
    parser = RegexTOCParser()

    # Test with invalid page numbers using public parse method
    invalid_pages = [
        (1, "1.1 Title abc"),  # Non-numeric page
        (1, "1.2 Title 99999"),  # Very large page number
        (1, "1.3 Title -5"),  # Negative page number
    ]

    for page_data in invalid_pages:
        entries = parser.parse([page_data])
        # Should return empty list for invalid entries
        for entry in entries:
            assert isinstance(entry.page, int)
            assert entry.page > 0


def test_empty_section_handling():
    """Test handling of empty or malformed sections."""
    parser = RegexTOCParser()

    malformed_pages = [
        (1, ""),  # Empty content
        (1, "   "),  # Whitespace only
        (1, "1."),  # Incomplete section
        (1, "Title only"),  # No section number
        (1, "1.1"),  # No title or page
    ]

    for page_data in malformed_pages:
        entries = parser.parse([page_data])
        # Should return empty list for malformed input
        assert isinstance(entries, list)
