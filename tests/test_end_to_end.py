"""End-to-end tests for the complete USB PD parser pipeline."""

import tempfile
import json
# from pathlib import Path

# from src.app import USBPDParser
from src.models import PageContent, TOCEntry
from src.config import Config


def test_config_loading():
    """Test configuration loading functionality."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.yml', delete=False) as f:
        f.write("""
pdf_input_file: "test.pdf"
output_directory: "test_outputs"
toc_file: "test.jsonl"
ocr_fallback: true
max_pages: 100
""")
        f.flush()
        
        config = Config(f.name)
        assert str(config.pdf_input_file) == "test.pdf"
        assert config.ocr_fallback == True


def test_jsonl_serialization():
    """Test JSONL output format compliance."""
    page_content = PageContent(
        page=1, text="Sample text", image_count=0, table_count=1
    )
    
    toc_entry = TOCEntry(
        doc_title="Test Doc", section_id="1.1", title="Introduction",
        page=15, level=2, parent_id="1", full_path="1.1 Introduction"
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
        doc_title="Test", section_id="1.1", title="Test Section",
        page=15, level=2, full_path="1.1 Test Section"
    )
    assert entry.parent_id == "1"  # Should be inferred