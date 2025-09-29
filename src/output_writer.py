"""Output writing with different formats."""

import json
from pathlib import Path
from typing import Any, Dict, List, Union

from .models import ContentItem, TOCEntry


class OutputWriter:
    """Handles saving results in various formats with single responsibility."""

    def __init__(self, output_dir: str = "outputs"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def write_toc_jsonl(
        self, toc_entries: List[TOCEntry], filename: str = "usb_pd_toc.jsonl"
    ) -> Path:
        """Write TOC entries to JSONL format."""
        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            for entry in toc_entries:
                json_line = entry.model_dump_json()
                f.write(json_line + "\n")

        return output_path

    def write_content_jsonl(
        self, content_items: List[ContentItem], filename: str = "usb_pd_spec.jsonl"
    ) -> Path:
        """Write content items to JSONL format."""
        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            for item in content_items:
                json_line = item.model_dump_json()
                f.write(json_line + "\n")

        return output_path

    def write_summary_json(
        self, summary_data: Dict[str, Any], filename: str = "extraction_summary.json"
    ) -> Path:
        """Write extraction summary to JSON format."""
        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)

        return output_path

    def write_text_report(
        self, data: Dict[str, Any], filename: str = "extraction_report.txt"
    ) -> Path:
        """Write human-readable text report."""
        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write("PDF Extraction Report\n")
            f.write("=" * 50 + "\n\n")

            # Document info
            if "document_info" in data:
                f.write("Document Information:\n")
                for key, value in data["document_info"].items():
                    f.write(f"  {key.title()}: {value}\n")
                f.write("\n")

            # Extraction stats
            if "stats" in data:
                f.write("Extraction Statistics:\n")
                for key, value in data["stats"].items():
                    f.write(f"  {key.replace('_', ' ').title()}: {value}\n")
                f.write("\n")

            # TOC summary
            if "toc_entries" in data:
                f.write(f"Table of Contents ({len(data['toc_entries'])} entries):\n")
                for entry in data["toc_entries"][:10]:  # First 10 entries
                    indent = "  " * (entry.level - 1) if hasattr(entry, "level") else ""
                    title = entry.title if hasattr(entry, "title") else str(entry)
                    f.write(f"{indent}- {title}\n")
                if len(data["toc_entries"]) > 10:
                    f.write(f"  ... and {len(data['toc_entries']) - 10} more entries\n")

        return output_path

    def write_all_formats(self, extraction_data: Dict[str, Any]) -> Dict[str, Path]:
        """Write extraction results in all supported formats."""
        output_files = {}

        # Write TOC
        if "toc" in extraction_data:
            output_files["toc_jsonl"] = self.write_toc_jsonl(extraction_data["toc"])

        # Write content
        if "content" in extraction_data:
            output_files["content_jsonl"] = self.write_content_jsonl(
                extraction_data["content"]
            )

        # Write summary
        summary_data = {
            "extraction_stats": {
                "total_pages": extraction_data.get("total_pages", 0),
                "toc_entries": len(extraction_data.get("toc", [])),
                "content_items": len(extraction_data.get("content", [])),
                "extraction_time": extraction_data.get("extraction_time", 0),
            },
            "document_info": extraction_data.get("document_info", {}),
            "files_created": [],
        }
        output_files["summary_json"] = self.write_summary_json(summary_data)

        # Write text report
        output_files["text_report"] = self.write_text_report(
            {
                "document_info": extraction_data.get("document_info", {}),
                "stats": summary_data["extraction_stats"],
                "toc_entries": extraction_data.get("toc", []),
            }
        )

        return output_files

    def get_output_stats(self) -> Dict[str, Any]:
        """Get statistics about output files."""
        stats = {
            "output_directory": str(self.output_dir),
            "files_created": [],
            "total_size_bytes": 0,
        }

        for file_path in self.output_dir.glob("*"):
            if file_path.is_file():
                file_stats = {
                    "filename": file_path.name,
                    "size_bytes": file_path.stat().st_size,
                    "format": file_path.suffix[1:] if file_path.suffix else "unknown",
                }
                stats["files_created"].append(file_stats)
                stats["total_size_bytes"] += file_stats["size_bytes"]

        return stats
