"""Pipeline orchestrator with OOP principles."""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple
from .config import Config
from .pdf_extractor import PDFExtractor
from .toc_extractor import TOCExtractor
from .output_writer import JSONLWriter
from .report_generator import ReportFactory


class BasePipeline(ABC):  # Abstraction
    """Abstract pipeline (Abstraction, Encapsulation)."""
    
    def __init__(self, config: Config):
        self._config = config  # Encapsulation
        self._logger = logging.getLogger(self.__class__.__name__)
        self._setup()
    
    def _setup(self) -> None:  # Encapsulation
        self._config.output_directory.mkdir(exist_ok=True)
        log_file = self._config.output_directory / "parser.log"
        handler = logging.FileHandler(log_file, mode='w')
        handler.setLevel(logging.INFO)
        logging.getLogger().addHandler(handler)
    
    @abstractmethod  # Abstraction
    def run(self, **kwargs: Any) -> Dict[str, Any]:
        pass


class PipelineOrchestrator(BasePipeline):  # Inheritance
    """Main orchestrator (Inheritance, Polymorphism)."""
    
    def __init__(self, config_path: str = "application.yml", 
                 debug: bool = False):
        super().__init__(Config(config_path))  # Inheritance
        if debug:
            logging.basicConfig(level=logging.DEBUG)
    
    def run(self, mode: int = 1, **kwargs: Any) -> Dict[str, Any]:  # Polymorphism
        """Run pipeline (Polymorphism)."""
        max_pages = None if mode == 1 else (600 if mode == 2 else 200)
        
        # Extract
        toc = TOCExtractor().extract_toc(self._config.pdf_input_file)
        content = PDFExtractor(self._config.pdf_input_file).extract_content(
            self._config.pdf_input_file, max_pages
        )
        
        # Write files
        toc_path = self._config.output_directory / "usb_pd_toc.jsonl"
        spec_path = self._config.output_directory / "usb_pd_spec.jsonl"
        JSONLWriter(toc_path).write_entries(toc)
        JSONLWriter(spec_path).write_content(content)
        
        # Generate reports
        counts = self._get_counts(content, toc, max_pages)  # Encapsulation
        reports = self._create_reports(counts)  # Encapsulation
        
        return {
            "toc_entries": len(toc),
            "toc_path": str(toc_path),
            "spec_path": str(spec_path),
            "report_path": str(reports[0]),
            "excel_path": str(reports[1]),
            "spec_counts": {"pages": counts["total_pages"], "paragraphs": counts["paragraphs"]},
        }
    
    def _get_counts(self, content: List[Dict[str, Any]], 
                   toc: List[Any], max_pages: Any) -> Dict[str, Any]:
        total_pages = max_pages or len(set(item.get("page", 0) for item in content))
        return {
            "total_pages": total_pages,
            "toc_entries": len(toc),
            "content_items": len(content),
            "paragraphs": sum(1 for item in content if item.get("type") == "paragraph"),
            "images": sum(1 for item in content if item.get("type") == "image"),
            "tables": sum(1 for item in content if item.get("type") == "table"),
        }
    
    def _create_reports(self, counts: Dict[str, Any]) -> Tuple[Any, Any]:  # Encapsulation
        json_gen = ReportFactory.create_generator(
            "json", self._config.output_directory
        )
        excel_gen = ReportFactory.create_generator(
            "excel", self._config.output_directory
        )
        return json_gen.generate(counts), excel_gen.generate(counts)
    
    def run_toc_only(self):  # Polymorphism
        return TOCExtractor().extract_toc(self._config.pdf_input_file)
    
    def run_content_only(self) -> int:  # Polymorphism
        content = PDFExtractor(self._config.pdf_input_file).extract_content(
            self._config.pdf_input_file
        )
        return len(content)
    
    def run_full_pipeline(self, mode: int = 1) -> Dict[str, Any]:  # Polymorphism
        return self.run(mode)