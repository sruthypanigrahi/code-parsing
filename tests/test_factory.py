"""Tests for factory classes."""

import pytest
from src.factory import ParserFactory
from src.parsing_strategies import RegexTOCParser, FuzzyTOCParser
from src.exceptions import ConfigurationError


class TestParserFactory:
    """Test parser factory."""

    def test_create_regex_parser(self):
        """Test creating regex parser."""
        parser = ParserFactory.create_parser("regex", "Test Doc")
        assert isinstance(parser, RegexTOCParser)
        assert parser.doc_title == "Test Doc"

    def test_create_fuzzy_parser(self):
        """Test creating fuzzy parser."""
        parser = ParserFactory.create_parser("fuzzy", "Test Doc")
        assert isinstance(parser, FuzzyTOCParser)
        assert parser.doc_title == "Test Doc"

    def test_create_unknown_parser(self):
        """Test creating unknown parser type."""
        with pytest.raises(ConfigurationError, match="Unknown parser type"):
            ParserFactory.create_parser("unknown", "Test Doc")

    def test_available_parsers(self):
        """Test getting available parsers."""
        parsers = ParserFactory.available_parsers()
        assert "regex" in parsers
        assert "fuzzy" in parsers
        assert len(parsers) >= 2
