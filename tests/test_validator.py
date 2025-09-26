"""Tests for the validation functionality."""

from src.models import TOCEntry
from src.validator import ValidationReport, Validator


def test_validation_report_creation():
    """Test ValidationReport creation and serialization."""
    report = ValidationReport()
    report.duplicates = ["1.1", "2.1"]
    report.total_entries = 10
    report.validation_passed = False

    report_dict = report.to_dict()
    assert report_dict["duplicates"] == ["1.1", "2.1"]
    assert not report_dict["validation_passed"]


def test_duplicate_detection():
    """Test detection of duplicate section IDs."""
    entries = [
        TOCEntry(
            doc_title="Test",
            section_id="1.1",
            title="First",
            page=10,
            level=2,
            full_path="1.1 First",
        ),
        TOCEntry(
            doc_title="Test",
            section_id="1.1",
            title="Second",
            page=20,
            level=2,
            full_path="1.1 Second",
        ),
    ]

    report = Validator.validate(entries)
    assert "1.1" in report.duplicates
    assert not report.validation_passed


def test_out_of_order_detection():
    """Test detection of out-of-order page numbers."""
    entries = [
        TOCEntry(
            doc_title="Test",
            section_id="1",
            title="First",
            page=10,
            level=1,
            full_path="1 First",
        ),
        TOCEntry(
            doc_title="Test",
            section_id="2",
            title="Second",
            page=30,
            level=1,
            full_path="2 Second",
        ),
        TOCEntry(
            doc_title="Test",
            section_id="3",
            title="Third",
            page=20,
            level=1,
            full_path="3 Third",  # Out of order
        ),
    ]

    report = Validator.validate(entries)
    assert "3" in report.out_of_order
    assert not report.validation_passed


def test_valid_entries_pass():
    """Test that valid entries pass validation."""
    entries = [
        TOCEntry(
            doc_title="Test",
            section_id="1",
            title="Introduction",
            page=10,
            level=1,
            parent_id=None,
            full_path="1 Introduction",
        ),
        TOCEntry(
            doc_title="Test",
            section_id="1.1",
            title="Overview",
            page=15,
            level=2,
            parent_id="1",
            full_path="1.1 Overview",
        ),
    ]

    report = Validator.validate(entries)
    assert report.validation_passed
    assert len(report.duplicates) == 0
