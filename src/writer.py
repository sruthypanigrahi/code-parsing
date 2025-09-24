
from typing import List
from pathlib import Path
from .models import TOCEntry


class JSONLWriter:
    """High-performance JSONL file writer with error handling.
    
    This class implements the Single Responsibility Principle by
    focusing solely on writing JSONL format files.
    """

    @staticmethod
    def write(entries: List[TOCEntry], output_file: Path) -> None:
        """Write TOC entries to JSONL file with performance optimization.
        
        Args:
            entries: List of TOCEntry objects to write
            output_file: Path to output JSONL file
            
        Raises:
            IOError: If file writing fails
        """
        JSONLWriter._ensure_output_directory(output_file)
        JSONLWriter._write_entries_batch(entries, output_file)
    
    @staticmethod
    def _ensure_output_directory(output_file: Path) -> None:
        """Ensure output directory exists.
        
        Args:
            output_file: Path to output file
        """
        output_file.parent.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def _write_entries_batch(entries: List[TOCEntry], output_file: Path) -> None:
        """Write entries in batch for better performance.
        
        Args:
            entries: List of TOCEntry objects
            output_file: Path to output file
        """
        with open(output_file, "w", encoding="utf-8", buffering=8192) as f:
            for entry in entries:
                f.write(entry.model_dump_json() + "\n")
