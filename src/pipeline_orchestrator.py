"""Simple pipeline orchestrator with OOP principles."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from .config import Config
from .pdf_extractor import PDFExtractor
from .toc_extractor import TOCExtractor
from .output_writer import JSONLWriter
from .report_generator import ReportFactory


class BasePipeline(ABC):  # Abstraction
    def __init__(self, config_path: str):
        try:
            self._config = Config(config_path)  # Encapsulation
        except (ValueError, OSError) as e:
            raise RuntimeError(f"Configuration error: {e}") from e
        try:
            self._config.output_directory.mkdir(parents=True, exist_ok=True)
        except (OSError, PermissionError) as e:
            raise RuntimeError(f"Cannot create output directory: {e}") from e
    
    @abstractmethod  # Abstraction
    def run(self, mode: int = 1) -> Dict[str, Any]:
        pass


class PipelineOrchestrator(BasePipeline):  # Inheritance
    def run(self, mode: int = 1) -> Dict[str, Any]:  # Polymorphism
        if mode == 1:
            max_pages: Optional[int] = None
        elif mode == 2:
            max_pages = 600
        else:
            max_pages = 200
        
        # Extract
        toc = TOCExtractor().extract_toc(self._config.pdf_input_file)
        content = PDFExtractor(self._config.pdf_input_file).extract_content(max_pages)
        
        # Write
        JSONLWriter(self._config.output_directory / "usb_pd_toc.jsonl").write(toc)
        JSONLWriter(self._config.output_directory / "usb_pd_spec.jsonl").write(content)
        
        # Reports
        counts = {
            "pages": len(content), 
            "content_items": len(content),
            "toc_entries": len(toc),
            "paragraphs": sum(
                1 for item in content 
                if item.get("type") == "paragraph"
            )
        }
        ReportFactory.create_generator(
            "json", self._config.output_directory
        ).generate(counts)
        ReportFactory.create_generator(
            "excel", self._config.output_directory
        ).generate(counts)
        
        # Validation report
        from .validation_generator import create_validation_report
        create_validation_report(
            self._config.output_directory,
            self._config.output_directory / "usb_pd_toc.jsonl",
            self._config.output_directory / "usb_pd_spec.jsonl"
        )
        
        return {"toc_entries": len(toc), "spec_counts": counts}
    
    def run_toc_only(self) -> Any:  # Polymorphism
        return TOCExtractor().extract_toc(self._config.pdf_input_file)
    
    def run_content_only(self) -> int:  # Polymorphism
        return len(PDFExtractor(self._config.pdf_input_file).extract_content())
    
    def run_full_pipeline(self, mode: int = 1) -> Dict[str, Any]:  # Polymorphism
        return self.run(mode)