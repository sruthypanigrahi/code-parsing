"""Tests for parsing strategies."""

import pytest
from src.parsing_strategies import RegexTOCParser, FuzzyTOCParser
from src.models import TOCEntry


class TestRegexTOCParser:
    """Test regex-based TOC parser."""

    def test_parse_lines_success(self):
        """Test successful line parsing."""
        parser = RegexTOCParser("Test Doc")
        lines = [
            "1.1 Introduction ........................... 15",
            "2.3.4 Advanced Topics ..................... 42",
        ]

        entries = list(parser.parse_lines(iter(lines)))
        assert len(entries) == 2

        assert entries[0].section_id == "1.1"
        assert entries[0].title == "Introduction"
        assert entries[0].page == 15
        assert entries[0].level == 2

        assert entries[1].section_id == "2.3.4"
        assert entries[1].title == "Advanced Topics"
        assert entries[1].page == 42
        assert entries[1].level == 3

    def test_parse_lines_no_matches(self):
        """Test parsing with no matching lines."""
        parser = RegexTOCParser("Test Doc")
        lines = ["Invalid line", "Another invalid line"]

        entries = list(parser.parse_lines(iter(lines)))
        assert len(entries) == 0

    def test_find_toc_lines(self):
        """Test TOC line detection."""
        parser = RegexTOCParser("Test Doc")
        pages = [
            "Some header text\n1.1 Introduction ........................... 15\n2.2 Methods ........................... 25\nFooter",
            "3.3 Results and discussion ........................... 35\nSome other text",
        ]

        toc_lines = list(parser.find_toc_lines(iter(pages)))
        expected_lines = [
            "1.1 Introduction ........................... 15",
            "2.2 Methods ........................... 25",
            "3.3 Results and discussion ........................... 35",
        ]
        assert toc_lines == expected_lines


class TestFuzzyTOCParser:
    """Test fuzzy TOC parser."""

    def test_parse_lines_success(self):
        """Test successful fuzzy parsing."""
        parser = FuzzyTOCParser("Test Doc")
        lines = ["1.1 Introduction 15", "2.3 Methods 42"]

        entries = list(parser.parse_lines(iter(lines)))
        assert len(entries) == 2
        assert entries[0].section_id == "1.1"
        assert entries[0].title == "Introduction"

    def test_parse_lines_skip_contents(self):
        """Test skipping contents header lines."""
        parser = FuzzyTOCParser("Test Doc")
        lines = ["Table of Contents", "1.1 Introduction 15"]

        entries = list(parser.parse_lines(iter(lines)))
        assert len(entries) == 1
        assert entries[0].section_id == "1.1"

    def test_exclude_month_names(self):
        """Test that month names are excluded."""
        parser = RegexTOCParser("Test Doc")
        lines = [
            "5 July 2012",  # Should be excluded
            "31 October 2012",  # Should be excluded
            "1.1 Introduction ........................... 15",  # Should be included
        ]

        toc_lines = list(parser.find_toc_lines(["\n".join(lines)]))
        entries = list(parser.parse_lines(iter(toc_lines)))

        # Only the real TOC entry should remain
        assert len(entries) == 1
        assert entries[0].section_id == "1.1"
        assert entries[0].title == "Introduction"
