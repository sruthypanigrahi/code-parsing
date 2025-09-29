"""USB PD Specification Parser - A modular PDF content extraction tool."""

__version__ = "1.0.0"
__author__ = "USB PD Parser Team"

from .models import TOCEntry
from .pipeline_orchestrator import PipelineOrchestrator

__all__ = [
    "PipelineOrchestrator", 
    "TOCEntry",
]