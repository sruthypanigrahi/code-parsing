#!/usr/bin/env python3
"""Create a minimal sample PDF for testing purposes."""

import logging
from pathlib import Path
from typing import Optional, Any

try:
    from src.logger import setup_logger  # type: ignore
except ImportError:
    def setup_logger(name: str, debug: bool = False) -> logging.Logger:  # type: ignore
        logger = logging.getLogger(name)
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG if debug else logging.INFO)
        return logger


class SamplePDFCreator:
    """Creates sample PDF files for testing the USB PD parser."""
    
    def __init__(self, output_dir: str = "assets", debug: bool = False):
        self.output_dir = Path(output_dir)
        self.logger: logging.Logger = setup_logger(__name__, debug=debug)
        
    def create_pdf(self, filename: str = "sample.pdf") -> Optional[Path]:
        """Create a sample PDF with TOC-like content."""
        try:
            from reportlab.pdfgen import canvas  # type: ignore
            from reportlab.lib.pagesizes import letter  # type: ignore
            
            output_path = self.output_dir / filename
            output_path.parent.mkdir(exist_ok=True)
            
            c = canvas.Canvas(str(output_path), pagesize=letter)
            width, height = letter
            
            self._create_content(c, width, height)
            c.save()
            
            self.logger.info(f"✅ Sample PDF created: {output_path}")
            return output_path
            
        except ImportError:
            return self._create_text_fallback(filename.replace('.pdf', '.txt'))
        except Exception as e:
            self.logger.error(f"Oops! Failed to create PDF: {e}")
            return None
    
    def _create_content(self, canvas_obj: Any, width: float, height: float) -> None:
        """Create PDF content with TOC."""
        # Title page
        canvas_obj.setFont("Helvetica-Bold", 16)
        canvas_obj.drawString(100, height - 100, "Sample Technical Document")
        
        # TOC entries
        canvas_obj.setFont("Helvetica", 11)
        toc_entries = [
            "1. Introduction  2", "1.1 Overview  2", "2. Technical Specifications  4"
        ]
        
        y_pos = height - 200
        for entry in toc_entries:
            canvas_obj.drawString(120, y_pos, entry)
            y_pos -= 20
        
        canvas_obj.showPage()
    
    def _create_text_fallback(self, filename: str) -> Optional[Path]:
        """Create text file when reportlab unavailable."""
        try:
            content = """Sample Technical Document
Table of Contents
1. Introduction  2
1.1 Overview  2
2. Technical Specifications  4"""
            
            output_path = self.output_dir / filename
            output_path.parent.mkdir(exist_ok=True)
            output_path.write_text(content)
            
            self.logger.info(f"📝 Sample text created: {output_path}")
            return output_path
            
        except Exception as e:
            self.logger.error(f"Oops! Failed to create text: {e}")
            return None


def main() -> None:
    """Main entry point."""
    try:
        creator = SamplePDFCreator(debug=True)
        result = creator.create_pdf()
        
        if result:
            print(f"✅ Sample file created: {result}")
        else:
            print("❌ Oops! Failed to create sample file")
            
    except Exception as e:
        print(f"❌ Oops! Unexpected error: {e}")


if __name__ == "__main__":
    main()