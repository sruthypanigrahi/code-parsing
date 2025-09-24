#!/usr/bin/env python3
"""Quick start demo for USB PD specification parser."""

import logging
from pathlib import Path
from typing import Optional

try:
    from src.logger import setup_logger  # type: ignore
    from src.app import USBPDParser
    from src.config import Config
except ImportError as e:
    print(f"❌ Oops! Import error: {e}")
    print("💡 Run from project root: python quick_start.py")
    exit(1)


class QuickStartDemo:
    """Quick demonstration of the USB PD parser."""
    
    def __init__(self, debug: bool = True):
        self.logger: logging.Logger = setup_logger(__name__, debug=debug)
        self.debug = debug
    
    def run_demo(self) -> bool:
        """Run the quick start demonstration."""
        try:
            self.logger.info("🚀 Starting USB PD Parser Quick Demo")
            
            # Check dependencies
            if not self._check_dependencies():
                return False
            
            # Find sample PDF
            pdf_path = self._find_sample_pdf()
            if not pdf_path:
                return False
            
            # Run parser
            return self._run_parser(pdf_path)
            
        except Exception as e:
            self.logger.error(f"Oops! Demo failed: {e}")
            return False
    
    def _check_dependencies(self) -> bool:
        """Check if required dependencies are available."""
        try:
            import pymupdf  # noqa: F401
            import pdfplumber  # noqa: F401
            self.logger.info("✅ Dependencies available")
            return True
        except ImportError as e:
            self.logger.error(f"Oops! Missing dependency: {e}")
            return False
    
    def _find_sample_pdf(self) -> Optional[Path]:
        """Find available sample PDF."""
        candidates = [
            Path("assets/USB_PD_R3_2 V1.1 2024-10.pdf"),
            Path("assets/sample.pdf")
        ]
        
        for pdf_path in candidates:
            if pdf_path.exists():
                self.logger.info(f"📄 Using PDF: {pdf_path}")
                return pdf_path
        
        self.logger.error("Oops! No sample PDF found")
        return None
    
    def _run_parser(self, pdf_path: Path) -> bool:
        """Run the parser on the sample PDF."""
        try:
            # Create temporary config
            config_content = f"""
pdf_input_file: "{pdf_path}"
output_directory: "outputs"
toc_file: "outputs/quick_demo.jsonl"
max_pages: 10
ocr_fallback: false
"""
            
            config_file = Path("temp_config.yml")
            config_file.write_text(config_content)
            
            # Run parser
            parser = USBPDParser(str(config_file), debug=self.debug)
            parser.run()
            
            # Cleanup
            config_file.unlink(missing_ok=True)
            
            self.logger.info("✅ Demo completed successfully!")
            return True
            
        except Exception as e:
            self.logger.error(f"Oops! Parser failed: {e}")
            return False


def main() -> None:
    """Main entry point for quick start demo."""
    try:
        demo = QuickStartDemo(debug=True)
        success = demo.run_demo()
        
        if success:
            print("🎉 Quick demo completed! Check outputs/quick_demo.jsonl")
        else:
            print("❌ Oops! Demo failed. Check logs for details.")
            
    except Exception as e:
        print(f"❌ Oops! Unexpected error: {e}")


if __name__ == "__main__":
    main()