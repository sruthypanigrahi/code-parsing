"""JSON Report Generator Module"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from src.support.report.report_generator import BaseReportGenerator


class JSONReportGenerator(BaseReportGenerator):  # Inheritance
    report_type = "json"
    file_extension = ".json"

    def _render(self, data: dict[str, Any]) -> Path:  # Polymorphism
        report_file = self.output_dir / "parsing_report.json"
        try:
            status = self._determine_validation_status(data)
            report: dict[str, Any] = {
                "metadata": {
                    "title": "USB PD Report",
                    "generated": datetime.now().isoformat(),
                },
                "summary": data,
                "validation": {"status": status},
            }
        except (TypeError, ValueError) as e:
            raise RuntimeError(f"Cannot create report data: {e}") from e
        try:
            with open(report_file, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)
        except OSError as e:
            raise RuntimeError(f"Cannot write JSON report: {e}") from e
        return report_file
