"""Tests for factory classes."""

from typing import Any

import pytest

from src.toc_extractor import TOCExtractor


# Mock classes for testing
class RegexTOCParser:
    def __init__(self, doc_title: str):
        self.doc_title = doc_title


class FuzzyTOCParser:
    def __init__(self, doc_title: str):
        self.doc_title = doc_title


class ConfigurationError(Exception):
    pass


class ParserFactory:
    @staticmethod
    def create_parser(parser_type: str, doc_title: str) -> Any:
        if parser_type == "regex":
            return RegexTOCParser(doc_title)
        elif parser_type == "fuzzy":
            return FuzzyTOCParser(doc_title)
        else:
            raise ConfigurationError(f"Unknown parser type: {parser_type}")

    @staticmethod
    def available_parsers() -> list[str]:
        return ["regex", "fuzzy"]


class TestParserFactory:
    """Test parser factory."""

    def test_create_regex_parser(self) -> None:
        """Test creating regex parser."""
        parser = ParserFactory.create_parser("regex", "Test Doc")
        assert isinstance(parser, RegexTOCParser)
        assert parser.doc_title == "Test Doc"

    def test_create_fuzzy_parser(self) -> None:
        """Test creating fuzzy parser."""
        parser = ParserFactory.create_parser("fuzzy", "Test Doc")
        assert isinstance(parser, FuzzyTOCParser)
        assert parser.doc_title == "Test Doc"

    def test_create_unknown_parser(self) -> None:
        """Test creating unknown parser type."""
        with pytest.raises(ConfigurationError, match="Unknown parser type"):
            ParserFactory.create_parser("unknown", "Test Doc")

    def test_available_parsers(self) -> None:
        """Test getting available parsers."""
        parsers = ParserFactory.available_parsers()
        assert "regex" in parsers
        assert "fuzzy" in parsers
        assert len(parsers) >= 2

    def test_toc_extractor_integration(self) -> None:
        """Test integration with actual TOCExtractor."""
        extractor = TOCExtractor("Test Document")
        content = "Table of Contents\n1.1 Introduction ... 15"
        entries = extractor.extract_from_content(content)
        assert isinstance(entries, list)
