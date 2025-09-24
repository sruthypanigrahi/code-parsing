"""USB PD Specification Parser - A modular PDF content extraction tool."""

__version__ = "1.0.0"
__author__ = "USB PD Parser Team"

from .config import Config
from .extractor import PDFExtractor
from .parser import TOCParser
from .writer import JSONLWriter
from .validator import Validator
from .models import PageContent, TOCEntry

__all__ = [
    "Config",
    "PDFExtractor", 
    "TOCParser",
    "JSONLWriter",
    "Validator",
    "PageContent",
    "TOCEntry"
]