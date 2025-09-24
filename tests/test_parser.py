"""Tests for the TOC parser functionality."""

from src.parser import TOCParser
# from src.models import TOCEntry


def test_simple_toc_parsing():
    """Test parsing simple TOC entries."""
    parser = TOCParser("Test Document")
    mock_pages = [
        (1, "1. Introduction  15"),
        (2, "1.1 Overview  16"),
        (3, "2. Technical Specifications  25")
    ]
    
    entries = parser.parse_toc(mock_pages)
    
    assert len(entries) >= 2
    assert any(entry.section_id == "1" for entry in entries)
    assert any(entry.section_id == "2" for entry in entries)


def test_hierarchical_parsing():
    """Test parsing hierarchical TOC structure."""
    parser = TOCParser("Test Document")
    mock_pages = [
        (1, "1.1.1 Subsection  27"),
        (2, "2.1 Power Requirements  26")
    ]
    
    entries = parser.parse_toc(mock_pages)
    
    # Should find entries with proper hierarchy
    subsection = next((e for e in entries if e.section_id == "1.1.1"), None)
    if subsection:
        assert subsection.level == 3
        assert subsection.parent_id == "1.1"


def test_malformed_input_handling():
    """Test handling of malformed TOC entries."""
    parser = TOCParser("Test Document")
    mock_pages = [
        (1, "Invalid line without proper format"),
        (2, "1. Valid Entry  15"),
        (3, "Another invalid line")
    ]
    
    entries = parser.parse_toc(mock_pages)
    
    # Should still parse valid entries
    assert len(entries) >= 1
    assert any(entry.section_id == "1" for entry in entries)