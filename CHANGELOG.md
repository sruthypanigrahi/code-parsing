# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Abstract base classes and protocols for better interface definition
- Comprehensive input validation with security checks
- Async processing capabilities for improved performance
- Progress tracking with visual progress bars
- Enhanced exception hierarchy with specific error types
- Comprehensive test suite with edge case coverage
- File size and type validation
- Unicode and special character handling
- Memory and timeout protection

### Enhanced
- Object-oriented architecture with proper encapsulation
- Type safety with full annotations
- Error handling with specific exceptions
- Security with input sanitization
- User experience with progress indicators

### Security
- Path traversal protection
- File size limits
- Input sanitization
- Dangerous character filtering

## [1.0.0] - 2024-01-XX

### Added
- Initial release with PDF parsing capabilities
- TOC extraction with pattern matching
- Content extraction (paragraphs, images, tables)
- Three extraction modes for different memory needs
- Interactive CLI interface
- Content search functionality
- JSONL output format
- Configuration management
- Performance monitoring
- Validation tools

### Features
- Processes 1047-page USB PD specification
- Extracts 149 TOC entries + 26,691 content items
- Smart image detection (>10x10px)
- Advanced table detection
- Fast content search
- Memory-efficient batch processing