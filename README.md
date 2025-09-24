# USB PD Specification Parser

A Python tool that extracts Table of Contents (ToC) from USB Power Delivery specification PDFs and converts them into structured JSONL format.

## Features

- **PDF Content Extraction**: Extracts text, images, and tables from PDF files
- **TOC Parsing**: Intelligent parsing of table of contents with multiple pattern matching
- **JSONL Output**: Structured output format for downstream processing
- **Validation**: Checks for duplicates and ordering issues
- **Performance Monitoring**: Tracks pages, words, images, and tables processed
- **Type Safety**: Full type hints with Pydantic models

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd code-parsing

# Install dependencies
pip install -r requirements.txt
```

## Usage

### Basic Usage
```bash
python main.py --input assets/sample.pdf --output outputs/out.jsonl
```

### With Configuration
```bash
python main.py --input assets/sample.pdf --output outputs/out.jsonl --config application.yml
```

## Sample Input → Output

**Input PDF**: USB Power Delivery Specification (1047 pages)

**Output Statistics**:
- Pages: 1047
- Words: 308,977
- Images: 4,814
- Tables: 3,239
- TOC Entries: 37

**Sample JSONL Output**:
```json
{"doc_title":"USB Power Delivery Specification","section_id":"1.1","title":"Introduction","page":15,"level":2,"parent_id":"1","full_path":"1.1 Introduction"}
{"doc_title":"USB Power Delivery Specification","section_id":"2.1.2","title":"Power Delivery Contract Negotiation","page":53,"level":3,"parent_id":"2.1","full_path":"2.1.2 Power Delivery Contract Negotiation"}
```

## Project Structure

```
code-parsing/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── app.py              # Main application orchestrator
│   ├── config.py           # Configuration management
│   ├── extractor.py        # PDF content extraction
│   ├── parser.py           # TOC parsing logic
│   ├── writer.py           # JSONL file writing
│   ├── validator.py        # Data validation
│   ├── models.py           # Pydantic data models
│   └── logger.py           # Logging configuration
├── tests/
│   └── test_parser.py      # Unit tests
├── main.py                 # CLI entry point
├── application.yml         # Configuration file
├── requirements.txt        # Dependencies
└── README.md              # This file
```

## Configuration

Edit `application.yml` to customize:
- Input PDF path
- Output directory
- OCR settings
- Processing limits

## License

MIT License - see LICENSE file for details.