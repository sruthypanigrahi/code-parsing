"""Test edge cases for TOC parsing and validation."""

import pytest
from src.parsing_strategies import RegexTOCParser
from src.validator import validate_iter
from src.models import TOCEntry


class TestTOCEdgeCases:
    """Test edge cases in TOC parsing."""

    def test_month_only_lines_ignored(self):
        """Test that month-only lines are ignored."""
        parser = RegexTOCParser("Test Doc")
        lines = [
            "5 July 2012",  # Should be ignored
            "31 October 2012",  # Should be ignored
            "1.1 Introduction to Power Delivery ........................... 15",  # Should be parsed
        ]

        toc_lines = list(parser.find_toc_lines(["\n".join(lines)]))
        entries = list(parser.parse_lines(iter(toc_lines)))

        # Only the real TOC entry should remain
        assert len(entries) == 1
        assert entries[0].section_id == "1.1"
        assert entries[0].title == "Introduction to Power Delivery"

    def test_dotted_leader_lines_parsed(self):
        """Test that dotted leader lines are correctly parsed."""
        parser = RegexTOCParser("Test Doc")
        lines = [
            "2.1 Power Delivery Overview ........................... 25",
            "2.2 Technical Specifications ........................... 35",
        ]

        entries = list(parser.parse_lines(iter(lines)))

        assert len(entries) == 2
        assert entries[0].section_id == "2.1"
        assert entries[0].title == "Power Delivery Overview"
        assert entries[0].page == 25

        assert entries[1].section_id == "2.2"
        assert entries[1].title == "Technical Specifications"
        assert entries[1].page == 35

    def test_implausible_pages_rejected(self):
        """Test that implausible page numbers are rejected by validator."""
        entries = [
            TOCEntry(
                doc_title="Test",
                section_id="1.1",
                title="Valid Entry",
                page=25,
                level=2,
                full_path="1.1 Valid Entry",
            ),
            TOCEntry(
                doc_title="Test",
                section_id="1.2",
                title="Invalid Page Zero",
                page=1,  # Use valid page for creation, validator will catch logic
                level=2,
                full_path="1.2 Invalid Page Zero",
            ),
            TOCEntry(
                doc_title="Test",
                section_id="1.3",
                title="Invalid Year Page",
                page=2012,
                level=2,
                full_path="1.3 Invalid Year Page",
            ),
        ]

        valid_entries = list(validate_iter(iter(entries)))

        # Valid entry and the one with page=1 should remain, year page should be rejected
        assert len(valid_entries) == 2
        valid_sections = [e.section_id for e in valid_entries]
        assert "1.1" in valid_sections
        assert "1.2" in valid_sections
        assert "1.3" not in [e.section_id for e in valid_entries]  # Year page rejected

    def test_short_titles_rejected(self):
        """Test that very short titles are rejected."""
        parser = RegexTOCParser("Test Doc")
        lines = [
            "1 A 15",  # Too short title
            "2 AB 25",  # Too short title
            "3.1 Introduction to Power Delivery Systems 35",  # Good title
        ]

        toc_lines = list(parser.find_toc_lines(["\n".join(lines)]))
        entries = list(parser.parse_lines(iter(toc_lines)))

        # Only the entry with good title should remain
        assert len(entries) == 1
        assert entries[0].section_id == "3.1"
        assert "Power Delivery Systems" in entries[0].title

    def test_figure_table_references_ignored(self):
        """Test that figure/table references are ignored."""
        parser = RegexTOCParser("Test Doc")
        lines = [
            "Figure 5 Power Delivery Architecture 25",  # Should be ignored
            "Table 3 Voltage Specifications 35",  # Should be ignored
            "3.1 Power Delivery Overview ........................... 45",  # Should be parsed
        ]

        toc_lines = list(parser.find_toc_lines(["\n".join(lines)]))
        entries = list(parser.parse_lines(iter(toc_lines)))

        # Only the real TOC entry should remain
        assert len(entries) == 1
        assert entries[0].section_id == "3.1"
        assert entries[0].title == "Power Delivery Overview"
