# USB PD Specification Parser

[![CI](https://github.com/username/usb-pd-parser/workflows/CI/badge.svg)](https://github.com/username/usb-pd-parser/actions)
[![Coverage](https://img.shields.io/codecov/c/github/username/usb-pd-parser)](https://codecov.io/gh/username/usb-pd-parser)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)

A high-performance Python tool that extracts complete content from USB Power Delivery specification PDFs, including Table of Contents, paragraphs, images, and tables. Features modular architecture with three extraction modes and comprehensive content detection.

## 🚀 Quick Start

```bash
# Clone and setup
git clone https://github.com/username/usb-pd-parser.git
cd usb-pd-parser
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Extract PDF content (interactive mode selection)
python main.py

# Extract with specific mode
python main.py --mode 1  # All pages (recommended)
python main.py --mode 2  # First 600 pages
python main.py --mode 3  # First 200 pages

# Extract only TOC or content
python main.py --toc-only
python main.py --content-only

# Search extracted content
python search_content.py "USB"
python search_content.py "Power Delivery" outputs/usb_pd_content.jsonl

# Run tests
pytest -q
```

## 📖 Getting Started Guide

### Step 1: Environment Setup

1. **Install Python 3.9+**
   ```bash
   python --version  # Should be 3.9 or higher
   ```

2. **Clone the Repository**
   ```bash
   git clone https://github.com/username/usb-pd-parser.git
   cd usb-pd-parser
   ```

3. **Create Virtual Environment**
   ```bash
   # Windows
   python -m venv .venv
   .venv\Scripts\activate
   
   # macOS/Linux
   python -m venv .venv
   source .venv/bin/activate
   ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Step 2: Prepare Your PDF

1. **Place PDF in assets folder**
   ```bash
   # Copy your USB PD specification PDF to:
   assets/USB_PD_R3_2 V1.1 2024-10.pdf
   ```

2. **Update Configuration (Optional)**
   ```bash
   # Copy example config
   cp application.example.yml application.yml
   
   # Edit application.yml to point to your PDF
   pdf_input_file: "assets/your-pdf-file.pdf"
   ```

### Step 3: Run the Extractor

#### Option A: Interactive Mode (Recommended for beginners)
```bash
python main.py
```
You'll see:
```
Choose extraction mode:
1. Full pipeline - Extract all pages with TOC and content (recommended)
2. Extract in 600-page batches (balanced)
3. Extract in 200-page batches (memory-safe)

Enter your choice (1, 2, or 3): 1
```

#### Option B: Direct Mode Selection
```bash
# Extract everything (best results)
python main.py --mode 1

# Extract first 600 pages (faster, good for testing)
python main.py --mode 2

# Extract first 200 pages (memory-safe)
python main.py --mode 3
```

#### Option C: Extract Specific Content
```bash
# Extract only Table of Contents
python main.py --toc-only

# Extract only content (paragraphs, images, tables)
python main.py --content-only
```

### Step 4: View Results

After extraction, you'll see:
```
Extraction completed successfully!
Total pages extracted: 1047
Paragraphs: 25760
Images: 196
Tables: 911
TOC entries: 149
Files created:
  - TOC: outputs\usb_pd_toc.jsonl
  - Content: outputs\usb_pd_content.jsonl
  - Spec: outputs\usb_pd_spec.jsonl
```

**Output Files:**
- `outputs/usb_pd_toc.jsonl` - Table of Contents entries (149 items)
- `outputs/usb_pd_content.jsonl` - All content items (26,691 items)
- `outputs/usb_pd_spec.jsonl` - Complete specification (all content)

### Step 5: Search Content

```bash
# Search for specific terms
python search_content.py "USB"           # Found 1,286 matches
python search_content.py "voltage"       # Found 820 matches
python search_content.py "Power Delivery" # Found 1,259 matches

# Search in specific file
python search_content.py "connector" outputs/usb_pd_content.jsonl
```

### Step 6: Troubleshooting

**Common Issues:**

1. **"PDF not found" error**
   ```bash
   # Check file path in application.yml
   pdf_input_file: "assets/USB_PD_R3_2 V1.1 2024-10.pdf"
   ```

2. **Memory issues with large PDFs**
   ```bash
   # Use smaller batch mode
   python main.py --mode 3  # 200 pages only
   ```

3. **No images found**
   ```bash
   # Images are mostly in later pages (1032+)
   # Use mode 1 to extract all pages
   python main.py --mode 1
   ```

4. **Enable debug logging**
   ```bash
   python main.py --debug --mode 1
   ```

## 📊 Sample Output

**Input**: USB Power Delivery Specification PDF (1047 pages)

**Extraction Results**:
- **Total pages**: 1,047
- **TOC entries**: 149
- **Paragraphs**: 25,760
- **Images**: 196
- **Tables**: 911

**Sample TOC Output** ([`usb_pd_toc.jsonl`](outputs/usb_pd_toc.jsonl)):
```json
{"doc_title":"USB_PD_R3_2 V1.1 2024-10.pdf","section_id":"S1","title":"Overview","full_path":"Overview","page":34,"level":1,"parent_id":null,"tags":[]}
{"doc_title":"USB_PD_R3_2 V1.1 2024-10.pdf","section_id":"S2","title":"Purpose","full_path":"Purpose","page":35,"level":1,"parent_id":null,"tags":[]}
```

**Sample Content Output** ([`usb_pd_content.jsonl`](outputs/usb_pd_content.jsonl)):
```json
{"doc_title":"USB_PD_R3_2 V1.1 2024-10.pdf","content_id":"C1","type":"paragraph","content":"Universal Serial Bus","page":1,"block_id":"p1_0","bbox":[171.33,62.91,423.95,95.74],"metadata":{"extracted_at":"2025-09-27T01:28:59.335084","content_length":20}}
{"doc_title":"USB_PD_R3_2 V1.1 2024-10.pdf","content_id":"C2","type":"image","content":"[Image 469x72 on page 1032]","page":1032,"block_id":"img1032_8","bbox":[71.74,260.98,540.26,332.54],"metadata":{"extracted_at":"2025-09-27T01:28:59.335084","content_length":27}}
{"doc_title":"USB_PD_R3_2 V1.1 2024-10.pdf","content_id":"C3","type":"table","content":"Table 2.1 Fixed Supply Power Ranges...","page":27,"block_id":"tbl27_0","bbox":[],"metadata":{"extracted_at":"2025-09-27T01:28:59.335084","content_length":156}}
```

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Dependencies
```bash
pip install -r requirements.txt
```

**Core Dependencies:**
- PyMuPDF (PDF processing)
- pdfplumber (Table extraction)
- Pydantic (Data validation)
- PyYAML (Configuration)

## 📋 Usage

### Command Line Interface

#### PDF Extraction
```bash
python main.py [OPTIONS]

Options:
  --config PATH    Configuration file path (default: application.yml)
  --debug          Enable debug logging
  --mode INT       Extraction mode: 1=all pages, 2=600 pages, 3=200 pages
  --toc-only       Extract only TOC entries
  --content-only   Extract only content (paragraphs, images, tables)
  --help           Show this message and exit

Interactive Mode:
  If no mode is specified, you'll be prompted to choose:
  1. Full pipeline - Extract all pages with TOC and content (recommended)
  2. Extract in 600-page batches (balanced)
  3. Extract in 200-page batches (memory-safe)
```

#### Content Search
```bash
python search_content.py <search_term> [jsonl_file]

Arguments:
  search_term      Text to search for in extracted content
  jsonl_file       Path to JSONL file (default: outputs/usb_pd_spec.jsonl)

Examples:
  python search_content.py "USB"                    # Found 1,286 matches
  python search_content.py "Power Delivery"         # Found 1,259 matches
  python search_content.py "voltage"                # Found 820 matches
```

### Configuration

Copy `application.example.yml` to `application.yml` and customize:

```yaml
# Input PDF file path
pdf_input_file: "assets/USB_PD_R3_2 V1.1 2024-10.pdf"

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

## 🏗️ Project Structure

```
usb-pd-parser/
├── 📁 src/                    # Core application modules (modular architecture)
│   ├── 🎯 pipeline_orchestrator.py # Main pipeline coordinator
│   ├── 📄 pdf_extractor.py    # PDF content extraction with image/table detection
│   ├── 🔍 toc_extractor.py    # TOC parsing with enhanced patterns
│   ├── 🔍 toc_pipeline.py     # TOC extraction pipeline
│   ├── 📊 content_processor.py # Content formatting and processing
│   ├── 📊 content_pipeline.py # Content extraction pipeline
│   ├── 🏗️  spec_builder.py    # Spec file builder with counting
│   ├── ⚙️  config.py          # YAML configuration loader
│   ├── 💾 writer.py           # JSONL output writer
│   ├── ✅ validator.py        # Data validation
│   ├── 📋 models.py           # Pydantic data models
│   ├── 📊 performance.py      # Performance monitoring
│   ├── 🗂️  cache.py           # Caching utilities
│   ├── 🚨 exceptions.py       # Custom exceptions
│   ├── 🔌 interfaces.py       # Protocol definitions
│   ├── 📝 logger.py           # Logging setup
│   └── 📄 extractor.py        # Legacy PDF utilities
├── 📁 assets/                 # Sample input files
├── 📁 outputs/                # Generated output files
│   ├── usb_pd_toc.jsonl      # Table of Contents entries
│   ├── usb_pd_content.jsonl  # All content (paragraphs, images, tables)
│   └── usb_pd_spec.jsonl     # Complete specification file
├── 🚀 main.py                 # CLI entry point with interactive mode
├── 🔍 search_content.py       # Content search utility with type hints
├── ⚙️  application.yml         # Configuration file
├── ⚙️  application.example.yml # Configuration template
├── 📦 requirements.txt        # Python dependencies
├── 📄 LICENSE                # MIT License
└── 📖 README.md              # This file
```

## 🚀 Features

- ✅ **Modular Architecture**: Clean separation into focused pipeline classes
- ✅ **Comprehensive Content Extraction**: Extracts paragraphs, images (>10x10px), and tables
- ✅ **Three Extraction Modes**: All pages, 600 pages, or 200 pages for different memory needs
- ✅ **Enhanced TOC Parsing**: 149 TOC entries with improved pattern matching
- ✅ **Smart Image Detection**: Filters meaningful images from decorative elements
- ✅ **Advanced Table Detection**: Multiple algorithms for table structure recognition
- ✅ **Type Safety**: Full type annotations with Pylance compatibility
- ✅ **Interactive CLI**: User-friendly mode selection with clear options
- ✅ **Fast Content Search**: Search 26,691+ content items with instant results
- ✅ **Performance Monitoring**: Built-in timing and metrics collection
- ✅ **Structured Output**: Three specialized JSONL files for different use cases

## 📈 Performance

- **Large PDFs**: Successfully processes 1047-page USB PD specification
- **Memory Efficient**: Three extraction modes for different memory constraints
- **Fast Processing**: ~14 seconds for full extraction (1047 pages)
- **Accurate Parsing**: 149 TOC entries + 26,691 content items extracted
- **Comprehensive Content**: Extracts paragraphs, images (>10x10px), and tables
- **Modular Architecture**: Clean separation of concerns for maintainability

## 🧪 Testing

### Quick Test
```bash
# Install test dependencies
pip install -r requirements-dev.txt

# Run tests (quick)
pytest --maxfail=1 --disable-warnings -q

# Run with coverage
coverage run -m pytest && coverage report -m
```

### Verify Installation
```bash
# Test with small extraction
python main.py --mode 3  # Extract first 200 pages

# Verify output files exist
ls outputs/
# Should show: usb_pd_toc.jsonl, usb_pd_content.jsonl, usb_pd_spec.jsonl

# Test search functionality
python search_content.py "USB"
# Should show: Found X matches for 'USB'
```

## 🛠️ Development

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run code formatting
black .

# Run linting
ruff check .

# Run type checking
mypy src --ignore-missing-imports

# Run all quality checks
black . && ruff check . && mypy src --ignore-missing-imports && pytest
```

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