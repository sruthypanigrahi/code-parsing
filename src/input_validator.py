"""Input validation utilities for enhanced security."""

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from .exceptions import InvalidInputError, PDFNotFoundError


class InputValidator:
    """Validates user inputs for security and correctness."""
    
    # File size limits (in bytes)
    MAX_PDF_SIZE = 500 * 1024 * 1024  # 500MB
    MAX_CONFIG_SIZE = 1024 * 1024     # 1MB
    
    # Allowed file extensions
    ALLOWED_PDF_EXTENSIONS = {'.pdf'}
    ALLOWED_CONFIG_EXTENSIONS = {'.yml', '.yaml'}
    
    @staticmethod
    def validate_pdf_path(pdf_path: Union[str, Path]) -> Path:
        """Validate PDF file path and properties."""
        path = Path(pdf_path).resolve()
        
        # Check if file exists
        if not path.exists():
            raise PDFNotFoundError(f"PDF file not found: {path}")
        
        # Check file extension
        if path.suffix.lower() not in InputValidator.ALLOWED_PDF_EXTENSIONS:
            raise InvalidInputError(f"Invalid file extension: {path.suffix}")
        
        # Check file size
        file_size = path.stat().st_size
        if file_size > InputValidator.MAX_PDF_SIZE:
            raise InvalidInputError(f"PDF file too large: {file_size} bytes")
        
        # Check if file is readable
        try:
            with open(path, 'rb') as f:
                header = f.read(4)
                if header != b'%PDF':
                    raise InvalidInputError("File is not a valid PDF")
        except PermissionError:
            raise InvalidInputError(f"Cannot read PDF file: {path}")
        
        return path
    
    @staticmethod
    def validate_config_path(config_path: Union[str, Path]) -> Path:
        """Validate configuration file path."""
        path = Path(config_path).resolve()
        
        if not path.exists():
            raise InvalidInputError(f"Config file not found: {path}")
        
        if path.suffix.lower() not in InputValidator.ALLOWED_CONFIG_EXTENSIONS:
            raise InvalidInputError(f"Invalid config extension: {path.suffix}")
        
        file_size = path.stat().st_size
        if file_size > InputValidator.MAX_CONFIG_SIZE:
            raise InvalidInputError(f"Config file too large: {file_size} bytes")
        
        return path
    
    @staticmethod
    def validate_search_term(search_term: str) -> str:
        """Validate search term for safety."""
        if not isinstance(search_term, str):
            raise InvalidInputError("Search term must be a string")
        
        if len(search_term.strip()) == 0:
            raise InvalidInputError("Search term cannot be empty")
        
        if len(search_term) > 1000:
            raise InvalidInputError("Search term too long (max 1000 characters)")
        
        # Remove potentially dangerous characters
        cleaned = re.sub(r'[<>"\'\\\x00-\x1f\x7f-\x9f]', '', search_term)
        return cleaned.strip()
    
    @staticmethod
    def validate_page_range(start_page: int, end_page: Optional[int] = None) -> tuple:
        """Validate page range parameters."""
        if not isinstance(start_page, int) or start_page < 1:
            raise InvalidInputError("Start page must be a positive integer")
        
        if end_page is not None:
            if not isinstance(end_page, int) or end_page < start_page:
                raise InvalidInputError("End page must be >= start page")
            
            if end_page - start_page > 10000:
                raise InvalidInputError("Page range too large (max 10000 pages)")
        
        return (start_page, end_page)
    
    @staticmethod
    def validate_output_directory(output_dir: Union[str, Path]) -> Path:
        """Validate and create output directory."""
        path = Path(output_dir).resolve()
        
        # Create directory if it doesn't exist
        try:
            path.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            raise InvalidInputError(f"Cannot create output directory: {path}")
        
        # Check if writable
        test_file = path / ".write_test"
        try:
            test_file.touch()
            test_file.unlink()
        except PermissionError:
            raise InvalidInputError(f"Output directory not writable: {path}")
        
        return path
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """Sanitize filename for safe file operations."""
        # Remove dangerous characters
        sanitized = re.sub(r'[<>:"/\\|?*\x00-\x1f\x7f-\x9f]', '_', filename)
        
        # Limit length
        if len(sanitized) > 255:
            sanitized = sanitized[:255]
        
        # Ensure not empty
        if not sanitized.strip():
            sanitized = "output"
        
        return sanitized.strip()