"""End-to-end tests for the complete USB PD parser pipeline."""

import json
import tempfile

from src.config import Config

# from pathlib import Path
# from src.app import USBPDParser
from src.models import PageContent, TOCEntry


def test_config_loading():
    """Test configuration loading functionality."""
    # Create dummy PDF file
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as pdf_file:
        pdf_path = pdf_file.name
    
    with tempfile.NamedTemporaryFile(mode="w", suffix=".yml", delete=False) as f:
        f.write(f"""pdf_input_file: {pdf_path.replace(chr(92), '/')}
output_directory: test_outputs
toc_file: test.jsonl
ocr_fallback: true
max_pages: 100
""")
        f.flush()

        config = Config(f.name)
        assert str(config.pdf_input_file) == pdf_path
        assert config.ocr_fallback
        
        # Cleanup
        import os
        try:
            os.unlink(pdf_path)
            os.unlink(f.name)
        except (PermissionError, FileNotFoundError):
            pass  # Ignore cleanup errors in tests


def test_jsonl_serialization():
    """Test JSONL output format compliance."""
    page_content = PageContent(page=1, text="Sample text", image_count=0, table_count=1)

    toc_entry = TOCEntry(
        doc_title="Test Doc",
        section_id="1.1",
        title="Introduction",
        page=15,
        level=2,
        parent_id="1",
        full_path="1.1 Introduction",
    )

    page_data = json.loads(page_content.model_dump_json())
    toc_data = json.loads(toc_entry.model_dump_json())

    assert page_data["page"] == 1
    assert toc_data["section_id"] == "1.1"


def test_model_validation():
    """Test Pydantic model validation."""
    page = PageContent(page=1, text="test", image_count=0, table_count=1)
    assert page.page == 1

    entry = TOCEntry(
        doc_title="Test",
        section_id="1.1",
        title="Test Section",
        page=15,
        level=2,
        parent_id="1",
        full_path="1.1 Test Section",
    )
    assert entry.parent_id == "1"
