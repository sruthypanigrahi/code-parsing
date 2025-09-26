# Architecture Guide

## Overview

The USB PD Parser follows a modular, pipeline-based architecture with clear separation of concerns and dependency injection.

## Core Components

### 1. Extraction Layer (`src/extractor.py`)
- **Purpose**: PDF content extraction
- **Key Functions**: `extract_front_pages()`, `get_doc_title()`
- **Dependencies**: PyMuPDF (fitz)
- **Caching**: Automatic caching of extracted content

### 2. Parsing Layer (`src/parsing_strategies.py`)
- **Purpose**: TOC entry parsing from text
- **Strategies**: Regex-based, Fuzzy matching
- **Pattern**: Strategy pattern with factory creation
- **Extensibility**: Easy to add new parsing strategies

### 3. Processing Layer (`src/hierarchy.py`, `src/validator.py`)
- **Purpose**: Data transformation and validation
- **Functions**: Hierarchy assignment, duplicate detection
- **Streaming**: Generator-based for memory efficiency

### 4. Output Layer (`src/writer.py`)
- **Purpose**: Structured output generation
- **Format**: JSONL with Pydantic validation
- **Streaming**: Memory-efficient writing

### 5. Orchestration Layer (`src/app.py`)
- **Purpose**: Pipeline coordination
- **Pattern**: Dependency injection
- **Monitoring**: Performance tracking and logging

## Design Patterns

### Factory Pattern
- `ParserFactory` creates parser instances
- Enables runtime strategy selection
- Supports plugin architecture

### Strategy Pattern
- Multiple parsing strategies (Regex, Fuzzy)
- Common interface via protocols
- Easy to extend and test

### Pipeline Pattern
- Streaming data flow: `pages → lines → entries → validated → output`
- Memory efficient processing
- Clear data transformations

### Protocol-Based Design
- Interfaces defined in `src/interfaces.py`
- Loose coupling between components
- Easy mocking for tests

## Performance Optimizations

### Caching
- File-based caching for expensive operations
- Automatic cache key generation
- Configurable cache directory

### Streaming Processing
- Generator-based pipeline
- Minimal memory footprint
- Early termination support

### Performance Monitoring
- Automatic timing of operations
- Metrics collection and reporting
- Bottleneck identification

## Error Handling

### Exception Hierarchy
- Custom exceptions in `src/exceptions.py`
- Proper error chaining
- Contextual error messages

### Robustness
- Graceful degradation
- Input validation
- Resource cleanup

## Extensibility

### Adding New Parsers
1. Implement `BaseTOCParser` interface
2. Register with `ParserFactory`
3. Add configuration option

### Adding New Output Formats
1. Implement `OutputWriter` protocol
2. Update factory or configuration
3. Maintain streaming interface

### Adding New Validation Rules
1. Extend `validate_iter()` function
2. Add new validation protocols
3. Maintain generator interface