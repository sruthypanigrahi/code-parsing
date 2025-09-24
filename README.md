# USB PD Specification Parser

## Overview
This project extracts the **Table of Contents (ToC)** from USB Power Delivery specification PDFs and converts it into structured **JSONL** format.

## Features
- Configurable via `application.yml`
- OOP design (`Config`, `PDFExtractor`, `TOCParser`, `JSONLWriter`, `Validator`)
- Modular codebase
- Type safety (Pydantic)
- OCR fallback for scanned PDFs
- JSONL output for downstream apps
- Validation checks (duplicates, order)

## Installation
```bash
pip install -r requirements.txt
