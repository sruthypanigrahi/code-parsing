# API Documentation

## Core Classes

### USBPDParser

Main orchestrator class for PDF parsing pipeline.

```python
from src.app import USBPDParser

# Initialize with config file
parser = USBPDParser("application.yml", debug=True)

# Initialize with dictionary
config = {
    "pdf_input_file": "document.pdf",
    "output": {"toc_file": "output.jsonl"}
}
parser = USBPDParser.from_dict(config)

# Run parsing pipeline
entries = parser.run()  # Returns List[TOCEntry]
```

### ContentExtractor

Handles PDF content extraction.

```python
from src.pipeline import ContentExtractor

extractor = ContentExtractor(
    pdf_path="document.pdf",
    output_dir="outputs",
    ocr_fallback=True,
    max_pages=100
)
pages = extractor.extract()  # Returns List[PageContent]
```

### TOCProcessor

Processes pages to extract TOC entries.

```python
from src.pipeline import TOCProcessor

processor = TOCProcessor("Document Title")
entries = processor.process(pages)  # Returns List[TOCEntry]
```

### Parsing Strategies

Strategy pattern for different parsing approaches.

```python
from src.parsing_strategies import RegexTOCParser, FuzzyTOCParser

# Regex-based parsing (default)
regex_parser = RegexTOCParser()
entries = regex_parser.parse(page_tuples)

# Fuzzy matching parsing
fuzzy_parser = FuzzyTOCParser()
entries = fuzzy_parser.parse(page_tuples)
```

### StreamingJSONLWriter

Memory-efficient writer for large documents.

```python
from src.streaming_writer import StreamingJSONLWriter
from pathlib import Path

# Context manager usage
with StreamingJSONLWriter(Path("output.jsonl")) as writer:
    for entry in entries:
        writer.write_entry(entry)

# Convenience method
StreamingJSONLWriter.write_streaming(entries, Path("output.jsonl"))
```

## Data Models

### TOCEntry

Represents a Table of Contents entry.

```python
from src.models import TOCEntry

entry = TOCEntry(
    doc_title="USB Power Delivery Specification",
    section_id="2.1.3",
    title="Power Requirements",
    page=45,
    level=3,
    full_path="2.1.3 Power Requirements",
    parent_id="2.1",  # Auto-inferred
    tags=[]
)
```

### PageContent

Represents extracted page content.

```python
from src.models import PageContent

page = PageContent(
    page=1,
    text="Page content text...",
    image_count=2,
    table_count=1
)
```

## Configuration

### YAML Configuration

```yaml
# application.yml
pdf_input_file: "assets/document.pdf"
output_directory: "outputs"
toc_file: "outputs/toc.jsonl"
ocr_fallback: true
max_pages: null  # Process all pages
```

### Programmatic Configuration

```python
config = {
    "pdf_input_file": "document.pdf",
    "output": {
        "toc_file": "output.jsonl",
        "output_directory": "outputs"
    },
    "extraction": {
        "max_pages": 100,
        "ocr_fallback": True
    }
}
```

## Error Handling

### Custom Exceptions

```python
from src.fuzzy_parser import ToCNotFoundError

try:
    entries = parser.parse(pages)
except ToCNotFoundError as e:
    print(f"No TOC found: {e}")
```

## Validation

### ValidationReport

```python
from src.validator import Validator

report = Validator.validate(entries)
print(f"Validation passed: {report.validation_passed}")
print(f"Duplicates: {report.duplicates}")
print(f"Out of order: {report.out_of_order}")
```