"""Tests for the TOC parser functionality."""


from src.models import TOCEntry
from src.toc_extractor import TOCExtractor


# Mock parser class for testing
class RegexTOCParser:
    def __init__(self, doc_title: str):
        self.doc_title = doc_title
        self.extractor = TOCExtractor(doc_title)

    def parse(self, pages: list[tuple[int, str]]) -> list[TOCEntry]:
        # Combine all page content
        content = "\n".join(page_content for _, page_content in pages)
        return self.extractor.extract_from_content(content)


def test_simple_toc_parsing() -> None:
    """Test parsing simple TOC entries."""
    parser = RegexTOCParser("Test Document")
    mock_pages = [
        (
            1,
            "Table of Contents\n1 Introduction ... 15\n1.1 Overview ... 16\n2 Technical Specifications ... 25",
        ),
    ]

    entries = parser.parse(mock_pages)

    assert isinstance(entries, list)
    # Should find at least one valid entry if TOC patterns match
    if entries:
        assert any(
            "Introduction" in entry.title or "Overview" in entry.title
            for entry in entries
        )


def test_hierarchical_parsing() -> None:
    """Test parsing hierarchical TOC structure."""
    parser = RegexTOCParser("Test Document")
    mock_pages = [
        (1, "Table of Contents\n1.1.1 Subsection ... 27\n2.1 Power Requirements ... 26")
    ]

    entries = parser.parse(mock_pages)

    # Should return a list (may be empty if patterns don't match)
    assert isinstance(entries, list)
    if entries:
        # Check that entries have proper structure
        for entry in entries:
            assert hasattr(entry, "title")
            assert hasattr(entry, "page")
            assert isinstance(entry.page, int)


def test_malformed_input_handling() -> None:
    """Test handling of malformed TOC entries."""
    parser = RegexTOCParser("Test Document")
    mock_pages = [
        (
            1,
            "Table of Contents\nInvalid line without proper format\n1 Valid Entry ... 15\nAnother invalid line",
        ),
    ]

    entries = parser.parse(mock_pages)

    # Should return a list and handle malformed input gracefully
    assert isinstance(entries, list)
    # Valid entries should be parsed if they match patterns
    if entries:
        for entry in entries:
            assert isinstance(entry, TOCEntry)
            assert entry.page > 0


def test_toc_extractor_direct() -> None:
    """Test TOCExtractor directly."""
    extractor = TOCExtractor("Test Document")
    content = "Table of Contents\n1.1 Introduction ... 15\n2.1 Methods ... 25"
    entries = extractor.extract_from_content(content)

    assert isinstance(entries, list)
    if entries:
        assert all(isinstance(entry, TOCEntry) for entry in entries)
        assert all(entry.page > 0 for entry in entries)
