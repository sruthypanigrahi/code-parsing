# USB PD Specification Parser

![Build Status](https://github.com/username/usb-pd-parser/workflows/CI/badge.svg)
![Coverage](https://img.shields.io/codecov/c/github/username/usb-pd-parser)
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![Type Checking](https://img.shields.io/badge/type%20checking-mypy-blue.svg)

A high-performance Python tool that extracts Table of Contents (ToC) from USB Power Delivery specification PDFs and converts them into structured JSONL format for downstream processing and analysis.

## What & Why

**What**: This tool processes large PDF specifications (like USB PD specs) to extract structured table of contents data, making it easier to navigate and analyze technical documents programmatically.

**Why**: Manual extraction of TOC data from large PDFs is time-consuming and error-prone. This tool automates the process with high accuracy and provides structured output for further analysis.

**How**: Uses advanced PDF parsing with multiple regex patterns, OCR fallback for scanned documents, and intelligent validation to ensure data quality.

## 🚀 Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/username/usb-pd-parser.git
cd usb-pd-parser

# 2. Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Copy and configure settings
cp application.example.yml application.yml
# Edit application.yml with your PDF path

# 5. Run the parser
python main.py

# Or with CLI arguments
python main.py --input assets/sample.pdf --output outputs/out.jsonl --debug

# 6. View results
cat outputs/out.jsonl | head -5
```

## 📊 Example Input → Output

**Input**: USB Power Delivery Specification PDF (1047 pages)

**Processing Stats**:
- ✅ Pages: 1,047 processed
- ✅ Words: 308,977 extracted  
- ✅ Images: 4,814 detected
- ✅ Tables: 3,239 found
- ✅ TOC Entries: 37 parsed

**Sample Input Text**:
```
1. Introduction  15
1.1 Overview  16
1.2 Scope  18
2. Technical Specifications  25
2.1 Power Requirements  26
2.1.1 Voltage Specifications  27
```

**Sample Output** ([`assets/sample_output.jsonl`](assets/sample_output.jsonl)):
```json
{"page":1,"text":"Universal Serial Bus\nPower Delivery Specification\nRevision: 3.2\nVersion: 1.1","image_count":0,"table_count":0}
{"doc_title":"USB Power Delivery Specification","section_id":"1","title":"Introduction","page":15,"level":1,"parent_id":null,"full_path":"1 Introduction"}
{"doc_title":"USB Power Delivery Specification","section_id":"1.1","title":"Overview","page":16,"level":2,"parent_id":"1","full_path":"1.1 Overview"}
{"doc_title":"USB Power Delivery Specification","section_id":"2.1.1","title":"Voltage Specifications","page":27,"level":3,"parent_id":"2.1","full_path":"2.1.1 Voltage Specifications"}
```

**Validation Report**:
```json
{
  "duplicates": [],
  "out_of_order": [],
  "missing_pages": [],
  "total_entries": 8,
  "validation_passed": true
}
```

## 🏗️ Project Structure

```
usb-pd-parser/
├── 📁 src/                    # Core application modules
│   ├── 🐍 __init__.py         # Package initialization
│   ├── 🎯 app.py              # Main orchestrator (USBPDParser class)
│   ├── ⚙️  config.py           # YAML configuration loader
│   ├── 📄 extractor.py        # PDF content extraction (PDFExtractor)
│   ├── 🔍 parser.py           # TOC parsing logic (TOCParser)
│   ├── 💾 writer.py           # JSONL output writer (JSONLWriter)
│   ├── ✅ validator.py        # Data validation (Validator)
│   ├── 📋 models.py           # Pydantic data models
│   ├── 📊 performance.py      # Performance monitoring
│   └── 📝 logger.py           # Logging setup
├── 🧪 tests/                  # Test suite
│   └── test_parser.py         # Unit tests
├── 📁 assets/                 # Sample input files
├── 📁 outputs/                # Generated output files
├── 🚀 main.py                 # CLI entry point
├── ⚙️  application.yml         # Configuration file
├── 📦 requirements.txt        # Python dependencies
└── 📖 README.md              # This file
```

## 🔧 Configuration

Copy `application.example.yml` to `application.yml` and customize:

```yaml
# Input PDF file path
pdf_input_file: "assets/usb_pd_spec.pdf"

# Output settings
output_directory: "outputs"
toc_file: "outputs/usb_pd_spec.jsonl"

# Processing options
ocr_fallback: true        # Enable OCR for scanned PDFs
max_pages: null          # Process all pages (or set limit)

# Parser settings
parser:
  min_line_length: 5     # Minimum line length for TOC parsing
  deduplicate: true      # Remove duplicate entries
```

## 🧪 Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html --cov-report=term

# Run specific test class
pytest tests/test_parser.py::TestTOCParser -v

# Run end-to-end tests
pytest tests/test_end_to_end.py -v

# View coverage report
open htmlcov/index.html  # On Windows: start htmlcov/index.html
```

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements.txt

# Run code formatting
black .

# Run linting
ruff check .

# Run type checking
mypy src --ignore-missing-imports

# Run all quality checks
black . && ruff check . && mypy src --ignore-missing-imports && pytest
```

## 📋 JSONL Schema

### Page Content
```json
{
  "page": 1,
  "text": "Page content text",
  "image_count": 0,
  "table_count": 2
}
```

### TOC Entry
```json
{
  "doc_title": "USB Power Delivery Specification",
  "section_id": "2.1.2",
  "title": "Power Delivery Contract Negotiation",
  "page": 53,
  "level": 3,
  "parent_id": "2.1",
  "full_path": "2.1.2 Power Delivery Contract Negotiation"
}
```

## 🚀 Features

- ✅ **High Performance**: Processes 1000+ page PDFs efficiently with streaming
- ✅ **OCR Support**: Handles scanned PDFs with Tesseract integration
- ✅ **Smart Parsing**: Multiple regex patterns for different TOC formats
- ✅ **Data Validation**: Detects duplicates, missing pages, and ordering issues
- ✅ **Type Safety**: Full type hints with Pydantic models and mypy checking
- ✅ **Comprehensive Logging**: Structured logging with debug mode
- ✅ **Configurable**: YAML-based configuration with CLI overrides
- ✅ **CLI Interface**: Easy command-line usage with --debug option
- ✅ **Well Tested**: Unit tests, edge cases, and end-to-end pipeline tests
- ✅ **CI/CD Ready**: GitHub Actions with coverage, security, and quality checks
- ✅ **Docker Support**: Containerized deployment with Tesseract OCR
- ✅ **Security Focused**: Bandit security scanning and dependency vulnerability checks

## 📈 Performance

- **Large PDFs**: Handles 1000+ page documents
- **Memory Efficient**: Streams content to avoid memory issues
- **Fast Processing**: ~4 minutes for 1047-page USB PD spec
- **Accurate Parsing**: 37/37 TOC entries extracted successfully

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- USB Implementers Forum for the USB PD specification
- PyMuPDF and pdfplumber communities for excellent PDF processing libraries