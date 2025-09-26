"""Performance tests for USB PD Parser."""

import time

import pytest

# from pathlib import Path
from src.pipeline_orchestrator import PipelineOrchestrator


@pytest.mark.performance
def test_pipeline_performance():
    """Test that pipeline runs within expected time."""
    # Use mode 3 (200 pages) for performance test
    orchestrator = PipelineOrchestrator("application.yml")

    start_time = time.time()
    results = orchestrator.run_full_pipeline(mode=3)
    duration = time.time() - start_time

    # Assert reasonable performance (adjust based on your requirements)
    assert duration < 60, f"Pipeline took {duration:.2f}s, expected < 60s"
    assert results["content_items"] > 0, "Should extract some content"
    assert results["toc_entries"] > 0, "Should extract some TOC entries"


@pytest.mark.performance
def test_toc_extraction_performance():
    """Test TOC extraction performance."""
    orchestrator = PipelineOrchestrator("application.yml")

    start_time = time.time()
    entries = orchestrator.run_toc_only()
    duration = time.time() - start_time

    # TOC extraction should be fast
    assert duration < 10, f"TOC extraction took {duration:.2f}s, expected < 10s"
    assert len(entries) > 0, "Should extract some TOC entries"


@pytest.mark.performance
def test_content_extraction_performance():
    """Test content extraction performance."""
    orchestrator = PipelineOrchestrator("application.yml")

    start_time = time.time()
    count = orchestrator.run_content_only()
    duration = time.time() - start_time

    # Content extraction should complete in reasonable time
    assert duration < 50, f"Content extraction took {duration:.2f}s, expected < 50s"
    assert count > 0, "Should extract some content items"
