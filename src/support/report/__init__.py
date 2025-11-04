"""Report generation module."""

from .report_generator import BaseReportGenerator, ReportFactory
from .excel_report import ExcelReportGenerator
from .jsonreport_generator import JSONReportGenerator

# Register generators after imports
ReportFactory.register("excel", ExcelReportGenerator)
ReportFactory.register("json", JSONReportGenerator)

__all__ = [
    "ExcelReportGenerator",
    "JSONReportGenerator",
    "ReportFactory",
    "BaseReportGenerator",
]
