# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive Google-style docstrings for all classes and methods
- Pre-commit hooks for code quality (black, ruff, isort, mypy)
- CONTRIBUTING.md with development guidelines
- Performance monitoring and optimization utilities
- Enhanced README with badges, project structure, and examples
- CI/CD pipeline with GitHub Actions
- Type safety with comprehensive type hints
- JSONL schema documentation

### Changed
- Improved error handling with specific exception types
- Enhanced logging with structured output
- Optimized PDF processing for large documents
- Refactored main.py to minimal CLI entry point

### Fixed
- Memory optimization for large PDF processing
- Type annotation issues throughout codebase
- Validation logic for TOC entries

## [1.0.0] - 2024-10-24

### Added
- Initial release of USB PD Specification Parser
- PDF content extraction with PyMuPDF and pdfplumber
- Table of Contents parsing with multiple regex patterns
- JSONL output format for structured data
- Pydantic models for type safety
- Configuration management with YAML
- Comprehensive test suite
- Data validation for duplicates and ordering
- Performance monitoring and statistics
- OCR fallback support for scanned PDFs

### Features
- Processes 1000+ page PDFs efficiently
- Extracts text, images, and table counts
- Intelligent TOC parsing with pattern matching
- Hierarchical section relationship inference
- Duplicate detection and removal
- Configurable processing limits
- Detailed logging and error reporting