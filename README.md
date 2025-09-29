# USB PD Specification Parser

A professional Python tool that extracts content from USB Power Delivery specification PDFs with comprehensive OOP design, generating multiple output formats including JSONL, JSON reports, and Excel validation files.

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run extraction (Interactive mode)
python main.py

# View results
head -n 3 outputs/usb_pd_spec.jsonl
```

## 📦 Installation

```bash
git clone https://github.com/sruthypanigrahi/code-parsing.git
cd code-parsing
pip install -r requirements.txt
```

## 💻 Usage

```bash
# Interactive mode (recommended)
python main.py

# Extract all pages
python main.py --mode 1

# Extract first 600 pages
python main.py --mode 2

# Extract first 200 pages (memory-safe)
python main.py --mode 3

# Extract only TOC
python main.py --toc-only

# Extract only content
python main.py --content-only

# Search extracted content
python search.py "USB"
```

## 🏗️ Project Structure

```
code-parsing/
├── src/                       # Core modules (OOP design)
│   ├── app.py                # CLI interface
│   ├── config.py             # Configuration loader
│   ├── pipeline_orchestrator.py # Main coordinator
│   ├── pdf_extractor.py      # PDF content extraction
│   ├── toc_extractor.py      # TOC parsing
│   ├── output_writer.py      # JSONL output writer
│   ├── report_generator.py   # Report generators (NEW)
│   ├── search_content.py     # Search functionality (NEW)
│   ├── models.py             # Data models
│   ├── base.py               # Base classes
│   ├── extractor.py          # Extraction utilities
│   └── logger.py             # Logging setup
├── tests/                     # Comprehensive test suite
│   ├── conftest.py           # Test configuration
│   ├── test_comprehensive.py # Full integration tests
│   ├── test_edge_cases.py    # Edge case testing
│   ├── test_extractor.py     # Extractor tests
│   └── test_parser.py        # Parser tests
├── assets/                    # Input PDFs
├── outputs/                   # Generated files
├── main.py                    # Entry point
├── search.py                  # Content search utility (NEW)
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## 📊 Output Files

The tool generates **5 comprehensive output files**:

1. **`outputs/usb_pd_toc.jsonl`** - Table of Contents entries
2. **`outputs/usb_pd_spec.jsonl`** - Complete specification content
3. **`outputs/parsing_report.json`** - Professional JSON report with metadata
4. **`outputs/validation_report.xlsx`** - Excel validation report (mandatory)
5. **`outputs/parser.log`** - Detailed processing logs

### 🔄 Regenerating Output Files

To regenerate all output files including the validation Excel report:

```bash
# Generate all outputs (recommended)
python main.py --mode 3

# Files will be created in outputs/ directory
ls outputs/  # validation_report.xlsx will be included
```

## 🎯 Key Features

- **Professional OOP Design**: All 4 OOP principles (Abstraction, Encapsulation, Inheritance, Polymorphism)
- **Multiple Output Formats**: JSONL, JSON, Excel, and Log files
- **Comprehensive Testing**: Full test suite with edge cases
- **Memory Management**: Multiple processing modes for different memory constraints
- **Search Functionality**: Built-in content search with professional CLI
- **Error Handling**: Robust error handling and validation
- **Professional Reports**: Styled Excel reports with validation metrics

## 🔧 Dependencies

- **PyMuPDF==1.24.9** (PDF processing)
- **pdfplumber==0.10.3** (Table extraction)
- **Pydantic==2.5.2** (Data validation)
- **PyYAML==6.0.1** (Configuration)
- **click==8.1.7** (CLI interface)
- **openpyxl==3.1.2** (Excel report generation)

## 🏛️ Architecture

Built with professional OOP principles:

- **Abstraction**: Abstract base classes for extensibility
- **Encapsulation**: Protected attributes and private methods
- **Inheritance**: Hierarchical class structure
- **Polymorphism**: Method overriding and factory patterns

## 📈 Performance

- **Mode 1**: Full document processing
- **Mode 2**: First 600 pages (balanced)
- **Mode 3**: First 200 pages (memory-safe)

## 🔍 Search Functionality

```bash
# Search in extracted content
python search.py "Power Delivery"
python search.py "USB" outputs/usb_pd_spec.jsonl
```

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow OOP principles
4. Add comprehensive tests
5. Submit a pull request