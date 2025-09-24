# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Docker support with Tesseract OCR and Poppler utilities
- Comprehensive validation reports with JSON output
- Pre-commit hooks for code quality
- CI/CD pipeline with GitHub Actions
- Sample assets for quick testing

## [1.0.0] - 2024-01-15

### Added
- Initial release of USB PD Specification Parser
- PDF content extraction using PyMuPDF and pdfplumber
- Table of Contents parsing with multiple regex patterns
- JSONL output format for structured data
- Comprehensive validation system
- CLI interface with Click
- Type safety with Pydantic v2 models
- Logging system with debug mode
- Performance monitoring utilities
- Memory-efficient processing for large PDFs
- OCR fallback support for scanned documents
- Hierarchical TOC structure inference
- Duplicate detection and deduplication
- Configuration management with YAML
- Unit and integration test suite
- Coverage reporting with pytest-cov

### Features
- **High Performance**: Processes 1000+ page PDFs efficiently
- **Smart Parsing**: Multiple regex patterns for different TOC formats
- **Data Validation**: Detects duplicates, missing pages, ordering issues
- **Type Safety**: Full type hints with Pydantic models
- **CLI Interface**: Easy command-line usage with multiple options
- **Configurable**: YAML-based configuration with CLI overrides
- **Well Tested**: Comprehensive test suite with 85%+ coverage

### Supported Formats
- PDF documents with text-based TOC
- Scanned PDFs with OCR fallback
- Various TOC formatting styles
- Hierarchical section numbering (1.1, 1.1.1, etc.)

### Dependencies
- Python 3.9+
- PyMuPDF (fitz) for PDF processing
- pdfplumber for table extraction
- Pydantic v2 for data validation
- Click for CLI interface
- PyYAML for configuration
- Optional: Tesseract for OCR support

## [0.2.0] - 2024-01-10

### Added
- Enhanced parser with multiple regex patterns
- Validation system for TOC entries
- Performance monitoring
- Memory optimization utilities

### Changed
- Improved error handling
- Better logging system
- Refactored modular architecture

### Fixed
- Memory leaks in large PDF processing
- Regex pattern edge cases
- Configuration loading issues

## [0.1.0] - 2024-01-05

### Added
- Basic PDF text extraction
- Simple TOC parsing
- JSONL output format
- Initial CLI interface
- Basic test suite

### Known Issues
- Limited TOC format support
- No validation system
- Basic error handling