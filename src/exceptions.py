"""Custom exceptions for USB PD Parser."""


class USBPDParserError(Exception):
    """Base exception for USB PD Parser."""
    pass


class PDFExtractionError(USBPDParserError):
    """Raised when PDF extraction fails."""
    pass


class TOCExtractionError(USBPDParserError):
    """Raised when TOC extraction fails."""
    pass


class ContentProcessingError(USBPDParserError):
    """Raised when content processing fails."""
    pass


class ValidationError(USBPDParserError):
    """Raised when validation fails."""
    pass


class ConfigurationError(USBPDParserError):
    """Raised when configuration is invalid."""
    pass


class PDFNotFoundError(USBPDParserError):
    """Raised when PDF file is not found."""
    pass


class InvalidInputError(USBPDParserError):
    """Raised when input data is invalid."""
    pass


class ProcessingTimeoutError(USBPDParserError):
    """Raised when processing takes too long."""
    pass


class MemoryLimitError(USBPDParserError):
    """Raised when memory limits are exceeded."""
    pass


class OutputWriteError(USBPDParserError):
    """Raised when output writing fails."""
    pass