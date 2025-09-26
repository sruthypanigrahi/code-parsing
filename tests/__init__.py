"""Test package for USB PD parser.

This package contains unit and integration tests for the USB Power Delivery
specification parser. Tests are organized by module and functionality.

Test Structure:
- test_parser.py: TOC parsing functionality
- test_validator.py: Validation logic
- test_end_to_end.py: Integration tests
- conftest.py: Shared fixtures

Usage:
    pytest tests/                    # Run all tests
    pytest tests/test_parser.py      # Run parser tests only
    pytest -v                       # Verbose output
    pytest --cov=src                # With coverage
"""

__version__ = "1.0.0"
__author__ = "USB PD Parser Team"

# Test configuration
TEST_DATA_DIR = "tests/fixtures"
SAMPLE_PDF = "assets/USB_PD_R3_2 V1.1 2024-10.pdf"


# Common test utilities
def create_mock_toc_entry(section_id: str = "1.1", title: str = "Test", page: int = 15):
    """Create a mock TOC entry for testing."""
    from src.models import TOCEntry

    return TOCEntry(
        doc_title="Test Document",
        section_id=section_id,
        title=title,
        page=page,
        level=len(section_id.split(".")),
        full_path=f"{section_id} {title}",
    )


def create_mock_page_content(page: int = 1, text: str = "Sample text"):
    """Create mock page content for testing."""
    from src.models import PageContent

    return PageContent(page=page, text=text, image_count=0, table_count=0)
