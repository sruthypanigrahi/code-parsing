# USB PD Specification Parser

A simple Python tool that extracts content from USB Power Delivery specification PDFs, including Table of Contents, paragraphs, images, and tables.

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run extraction
python main.py --mode 1

# View results
head -n 3 outputs/usb_pd_spec.jsonl
```

## Installation

```bash
git clone https://github.com/sruthypanigrahi/code-parsing.git
cd code-parsing
pip install -r requirements.txt
```

## Usage

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
python search_content.py "USB"
```

## Project Structure

```
code-parsing/
├── src/                       # Core modules
│   ├── app.py                # CLI interface
│   ├── config.py             # Configuration loader
│   ├── pipeline_orchestrator.py # Main coordinator
│   ├── pdf_extractor.py      # PDF content extraction
│   ├── toc_extractor.py      # TOC parsing
│   ├── output_writer.py      # JSONL output writer
│   ├── models.py             # Data models
│   └── logger.py             # Logging setup
├── assets/                    # Input PDFs
├── outputs/                   # Generated files
├── tests/                     # Test suite
├── main.py                    # Entry point
├── search_content.py          # Content search utility
├── requirements.txt           # Dependencies
└── README.md                  # This file
```

## Output

The tool generates two main files:
- `outputs/usb_pd_toc.jsonl` - Table of Contents entries
- `outputs/usb_pd_spec.jsonl` - Complete specification content

## Dependencies

- PyMuPDF==1.24.9 (PDF processing)
- pdfplumber==0.10.3 (Table extraction)
- Pydantic==2.5.2 (Data validation)
- PyYAML==6.0.1 (Configuration)
- click==8.1.7 (CLI interface)

## License

MIT License - see [LICENSE](LICENSE) file for details.