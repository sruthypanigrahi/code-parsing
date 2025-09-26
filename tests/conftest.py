"""Shared test fixtures and configuration."""

import pytest
from pathlib import Path
from typing import List
from src.models import TOCEntry, PageContent


@pytest.fixture
def sample_toc_entry() -> TOCEntry:
    """Standard TOC entry for testing."""
    return TOCEntry(
        doc_title="USB Power Delivery Specification",
        section_id="1",
        title="Introduction",
        page=15,
        level=1,
        full_path="1 Introduction",
    )


@pytest.fixture
def sample_toc_entries() -> List[TOCEntry]:
    """Multiple TOC entries for testing."""
    return [
        TOCEntry(
            doc_title="Test Doc",
            section_id="1",
            title="Introduction",
            page=15,
            level=1,
            full_path="1 Introduction",
        ),
        TOCEntry(
            doc_title="Test Doc",
            section_id="1.1",
            title="Overview",
            page=16,
            level=2,
            full_path="1.1 Overview",
        ),
        TOCEntry(
            doc_title="Test Doc",
            section_id="2",
            title="Technical Specifications",
            page=25,
            level=1,
            full_path="2 Technical Specifications",
        ),
    ]


@pytest.fixture
def sample_page_content() -> PageContent:
    """Sample page content for testing."""
    return PageContent(
        page=1,
        text="1. Introduction 15\n1.1 Overview 16\n2. Technical Specifications 25",
        image_count=0,
        table_count=1,
    )


@pytest.fixture
def test_output_dir(tmp_path: Path) -> Path:
    """Temporary output directory for tests."""
    output_dir: Path = tmp_path / "test_outputs"
    output_dir.mkdir(exist_ok=True)
    return output_dir
