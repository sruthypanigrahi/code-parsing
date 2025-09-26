from collections import Counter
from typing import Any, Dict, List, Set, Iterator
import logging
from .models import TOCEntry

logger = logging.getLogger(__name__)


def validate_iter(entries_iter: Iterator[TOCEntry]) -> Iterator[TOCEntry]:
    """Validate parsed objects and yield only valid entries.

    Args:
        entries_iter: Iterator of TOC entries to validate

    Yields:
        TOCEntry: Valid TOC entries only
    """
    seen_ids = set()
    dropped_count = 0

    for entry in entries_iter:
        try:
            # Validate using Pydantic model
            validated_entry = TOCEntry(**entry.model_dump())

            # Sanity check page numbers - much stricter
            if validated_entry.page <= 0 or validated_entry.page > 1500:
                logger.warning(
                    f"Invalid page number {validated_entry.page} for section {validated_entry.section_id}"
                )
                dropped_count += 1
                continue
                
            # Check for obviously wrong OCR artifacts
            if validated_entry.page > 999 and str(validated_entry.page).startswith(('20', '19')):
                logger.warning(
                    f"Suspicious page number {validated_entry.page} (looks like year) for section {validated_entry.section_id}"
                )
                dropped_count += 1
                continue

            # Check for duplicates
            if validated_entry.section_id in seen_ids:
                logger.warning(f"Duplicate section ID: {validated_entry.section_id}")
                dropped_count += 1
                continue

            seen_ids.add(validated_entry.section_id)
            yield validated_entry

        except Exception as e:
            logger.warning(f"Invalid TOC entry skipped: {e}")
            dropped_count += 1
            continue

    if dropped_count > 0:
        logger.info(f"Dropped {dropped_count} invalid entries during validation")


class ValidationReport:
    def __init__(self):
        self.duplicates: List[str] = []
        self.out_of_order: List[str] = []
        self.duplicate_pages: List[int] = []
        self.total_entries: int = 0
        self.validation_passed: bool = True

    def to_dict(self) -> Dict[str, Any]:
        return {
            "duplicates": self.duplicates,
            "out_of_order": self.out_of_order,
            "duplicate_pages": self.duplicate_pages,
            "total_entries": self.total_entries,
            "validation_passed": self.validation_passed,
        }


class Validator:
    @staticmethod
    def validate(entries: List[TOCEntry]) -> ValidationReport:
        report = ValidationReport()
        report.total_entries = len(entries)
        if not entries:
            return report

        report.duplicates = Validator._check_duplicates(entries)
        report.out_of_order = Validator._check_order(entries)
        report.duplicate_pages = Validator._check_duplicate_pages(entries)
        report.validation_passed = not any(
            [report.duplicates, report.out_of_order, report.duplicate_pages]
        )
        return report

    @staticmethod
    def _check_duplicates(entries: List[TOCEntry]) -> List[str]:
        seen: Set[str] = set()
        duplicates: List[str] = []
        for entry in entries:
            if entry.section_id in seen:
                duplicates.append(entry.section_id)
            seen.add(entry.section_id)
        return duplicates

    @staticmethod
    def _check_order(entries: List[TOCEntry]) -> List[str]:
        out_of_order: List[str] = []
        last_page = 0
        for entry in entries:
            if entry.page < last_page:
                out_of_order.append(entry.section_id)
            else:
                last_page = entry.page
        return out_of_order

    @staticmethod
    def _check_duplicate_pages(entries: List[TOCEntry]) -> List[int]:
        page_counts = Counter(entry.page for entry in entries)
        return [page for page, count in page_counts.items() if count > 1]
