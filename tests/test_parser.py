
from typing import List
from src.parser import TOCParser
from src.models import TOCEntry


class TestTOCParser:
    """Test suite for TOC parser functionality."""
    
    def __init__(self):
        self.parser = TOCParser(doc_title="USB PD Spec")
        self.sample_texts = [
            "2.1.2 Power Delivery Contract Negotiation  53",
            "2.1.2 Power Delivery Contract Negotiation .... 53",
            "2.1.2    Power Delivery Contract Negotiation    53"
        ]
    
    def test_parser_extracts_entry(self) -> None:
        """Test parser extracts TOC entries correctly."""
        for sample_text in self.sample_texts:
            entries = self.parser.parse_toc([(1, sample_text)])
            self._validate_entry(entries)
    
    def _validate_entry(self, entries: List[TOCEntry]) -> None:
        """Validate parsed entry properties."""
        assert len(entries) == 1
        e = entries[0]
        assert e.section_id == "2.1.2"
        assert "Power Delivery Contract Negotiation" in e.title
        assert e.page == 53
        assert e.level == 3
        assert e.parent_id == "2.1"


def test_parser_extracts_entry():
    """Function wrapper for class-based test."""
    test_suite = TestTOCParser()
    test_suite.test_parser_extracts_entry()
