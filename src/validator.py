from typing import List, Dict
from .models import TOCEntry


class Validator:
    """Validates parsed TOC entries."""

    @staticmethod
    def validate(entries: List[TOCEntry]) -> Dict[str, List[str]]:
        issues: Dict[str, List[str]] = {"duplicates": [], "out_of_order": []}

        seen_ids: set[str] = set()
        last_page = 0
        for entry in entries:
            if entry.section_id in seen_ids:
                issues["duplicates"].append(entry.section_id)
            seen_ids.add(entry.section_id)

            if entry.page < last_page:
                issues["out_of_order"].append(entry.section_id)
            last_page = entry.page

        return issues
