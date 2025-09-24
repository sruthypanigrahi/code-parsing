import json
from typing import List, Dict, Any, Set
from pathlib import Path
from .models import TOCEntry, PageContent


class ValidationReport:
    """Validation report with comprehensive issue tracking."""
    
    def __init__(self):
        self.duplicates: List[str] = []
        self.out_of_order: List[str] = []
        self.missing_pages: List[int] = []
        self.duplicate_pages: List[int] = []
        self.total_entries: int = 0
        self.validation_passed: bool = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert report to dictionary."""
        return {
            "duplicates": self.duplicates,
            "out_of_order": self.out_of_order,
            "missing_pages": self.missing_pages,
            "duplicate_pages": self.duplicate_pages,
            "total_entries": self.total_entries,
            "validation_passed": self.validation_passed
        }
    
    def to_json(self) -> str:
        """Convert report to JSON string."""
        return json.dumps(self.to_dict(), indent=2)
    
    def save_to_file(self, filepath: Path) -> None:
        """Save validation report to JSON file."""
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(self.to_json())


class Validator:
    """Validates parsed TOC entries and page content."""

    @staticmethod
    def validate(entries: List[TOCEntry]) -> Dict[str, List[str]]:
        """Legacy validation method for backward compatibility."""
        report = Validator.validate_comprehensive(entries)
        return {
            "duplicates": report.duplicates,
            "out_of_order": report.out_of_order
        }
    
    @staticmethod
    def validate_comprehensive(entries: List[TOCEntry], pages: List[PageContent] = None) -> ValidationReport:
        """Comprehensive validation with detailed reporting."""
        report = ValidationReport()
        report.total_entries = len(entries)
        
        if not entries:
            return report
        
        # Check for duplicate section IDs
        seen_ids: Set[str] = set()
        for entry in entries:
            if entry.section_id in seen_ids:
                report.duplicates.append(entry.section_id)
            seen_ids.add(entry.section_id)
        
        # Check for out-of-order pages
        last_page = 0
        for entry in entries:
            if entry.page < last_page:
                report.out_of_order.append(entry.section_id)
            last_page = entry.page
        
        # Check for duplicate page numbers in TOC entries
        page_counts: Dict[int, int] = {}
        for entry in entries:
            page_counts[entry.page] = page_counts.get(entry.page, 0) + 1
        
        report.duplicate_pages = [page for page, count in page_counts.items() if count > 1]
        
        # Check for missing pages if page content is provided
        if pages:
            toc_pages = {entry.page for entry in entries}
            content_pages = {page.page for page in pages}
            
            # Find pages referenced in TOC but missing from content
            max_content_page = max(content_pages) if content_pages else 0
            for toc_page in toc_pages:
                if toc_page <= max_content_page and toc_page not in content_pages:
                    report.missing_pages.append(toc_page)
        
        # Determine if validation passed
        report.validation_passed = (
            len(report.duplicates) == 0 and
            len(report.out_of_order) == 0 and
            len(report.missing_pages) == 0 and
            len(report.duplicate_pages) == 0
        )
        
        return report
    
    @staticmethod
    def validate_hierarchical_structure(entries: List[TOCEntry]) -> List[str]:
        """Validate hierarchical structure consistency."""
        issues: List[str] = []
        
        for entry in entries:
            if entry.parent_id:
                # Check if parent exists
                parent_exists = any(e.section_id == entry.parent_id for e in entries)
                if not parent_exists:
                    issues.append(f"Missing parent '{entry.parent_id}' for section '{entry.section_id}'")
                
                # Check level consistency
                expected_level = len(entry.section_id.split("."))
                if entry.level != expected_level:
                    issues.append(f"Inconsistent level for '{entry.section_id}': expected {expected_level}, got {entry.level}")
        

