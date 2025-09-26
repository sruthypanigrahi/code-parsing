"""Content extraction pipeline."""

from pathlib import Path
from .pdf_extractor import PDFExtractor
from .content_processor import ContentProcessor


class ContentPipeline:
    """Handles content extraction pipeline."""
    
    def __init__(self, config, logger):
        self.cfg = config
        self.logger = logger
    
    def extract_content(self, pdf_path: Path, max_pages=None) -> int:
        """Extract structured content from PDF."""
        pdf_extractor = PDFExtractor(pdf_path)
        doc_title = pdf_extractor.get_doc_title()
        
        # Extract structured content
        content_iterator = pdf_extractor.extract_structured_content(max_pages)
        content_processor = ContentProcessor(doc_title)
        processed_content = content_processor.process_structured_content(content_iterator)
        
        # Save content
        content_path = Path(self.cfg.output_directory) / "usb_pd_content.jsonl"
        content_count = content_processor.save_content(processed_content, content_path)
        
        self.logger.info(f"Extracted {content_count} content items to {content_path}")
        return content_count