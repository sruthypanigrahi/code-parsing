"""Report generator with OOP principles."""

import json
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict
from datetime import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill


class BaseReportGenerator(ABC):  # Abstraction
    """Abstract report generator (Abstraction, Encapsulation)."""
    
    def __init__(self, output_dir: Path):
        self._output_dir = output_dir  # Encapsulation
        self._timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @abstractmethod  # Abstraction
    def generate(self, data: Dict[str, Any]) -> Path:
        pass
    
    def _ensure_output_dir(self) -> None:  # Encapsulation
        self._output_dir.mkdir(parents=True, exist_ok=True)


class JSONReportGenerator(BaseReportGenerator):  # Inheritance
    """JSON report generator (Inheritance, Polymorphism)."""
    
    def generate(self, data: Dict[str, Any]) -> Path:  # Polymorphism
        self._ensure_output_dir()
        report_file = self._output_dir / "parsing_report.json"
        
        report: Dict[str, Any] = {
            "metadata": {
                "title": "USB PD Parsing Report", 
                "generated": self._timestamp, 
                "version": "1.0"
            },
            "summary": data,
            "validation": {
                "toc_ok": data.get("toc_entries", 0) > 0,
                "content_ok": data.get("content_items", 0) > 0,
                "images_ok": data.get("images", 0) >= 0,
                "tables_ok": data.get("tables", 0) >= 0
            }
        }
        
        with open(report_file, "w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        return report_file


class ExcelValidationGenerator(BaseReportGenerator):  # Inheritance
    """Excel validation generator (Inheritance, Polymorphism)."""
    
    def generate(self, data: Dict[str, Any]) -> Path:  # Polymorphism
        self._ensure_output_dir()
        excel_file = self._output_dir / "validation_report.xlsx"
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "USB PD Validation"  # type: ignore
        
        # Styling
        header_font = Font(bold=True, color="FFFFFF")
        header_fill = PatternFill(start_color="2F5597", end_color="2F5597", fill_type="solid")
        
        # Title
        ws['A1'] = "USB Power Delivery - Validation Report"  # type: ignore
        ws['A1'].font = Font(bold=True, size=14)  # type: ignore
        ws['A2'] = f"Generated: {self._timestamp}"  # type: ignore
        
        # Headers
        headers = ["Metric", "Count", "Status", "Quality"]
        for col, header in enumerate(headers, 1):
            cell = ws.cell(row=4, column=col, value=header)  # type: ignore
            cell.font = header_font  # type: ignore
            cell.fill = header_fill  # type: ignore
        
        # Data
        metrics = [
            ("Pages", data.get("total_pages", 0), "PASS" if data.get("total_pages", 0) > 0 else "FAIL", "Good"),
            ("TOC", data.get("toc_entries", 0), "PASS" if data.get("toc_entries", 0) > 0 else "FAIL", "Good"),
            ("Content", data.get("content_items", 0), "PASS" if data.get("content_items", 0) > 0 else "FAIL", "Good"),
        ]
        
        for row, (metric, value, status, quality) in enumerate(metrics, 5):
            ws.cell(row=row, column=1, value=metric)  # type: ignore
            ws.cell(row=row, column=2, value=value)  # type: ignore
            ws.cell(row=row, column=3, value=status)  # type: ignore
            ws.cell(row=row, column=4, value=quality)  # type: ignore
        
        wb.save(excel_file)
        return excel_file


class ReportFactory:  # Abstraction
    """Report factory (Abstraction, Encapsulation)."""
    
    @staticmethod  # Encapsulation
    def create_generator(report_type: str, output_dir: Path) -> BaseReportGenerator:
        if report_type == "json":
            return JSONReportGenerator(output_dir)  # Polymorphism
        elif report_type == "excel":
            return ExcelValidationGenerator(output_dir)  # Polymorphism
        else:
            return JSONReportGenerator(output_dir)  # Default