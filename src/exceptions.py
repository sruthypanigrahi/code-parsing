"""Custom exceptions for USB PD Parser."""


class USBPDParserError(Exception):
    """Base exception for USB PD Parser."""


class PDFNotFoundError(USBPDParserError):
    """Raised when PDF file is not found."""


class TOCNotFoundError(USBPDParserError):
    """Raised when no TOC entries are found."""


class ValidationError(USBPDParserError):
    """Raised when validation fails."""


class ConfigurationError(USBPDParserError):
    """Raised when configuration is invalid."""
