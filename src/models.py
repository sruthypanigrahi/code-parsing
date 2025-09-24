from typing import Optional, Any
from pydantic import BaseModel, field_validator, Field, ValidationInfo


class PageContent(BaseModel):
    """Represents content extracted from a single PDF page.
    
    Attributes:
        page: Page number (1-based)
        text: Extracted text content
        image_count: Number of images found on the page
        table_count: Number of tables found on the page
    """
    page: int = Field(gt=0, description="Page number (1-based)")
    text: str = Field(description="Extracted text content")
    image_count: int = Field(ge=0, description="Number of images on page")
    table_count: int = Field(ge=0, description="Number of tables on page")


class TOCEntry(BaseModel):
    """Represents a Table of Contents entry with hierarchical structure.
    
    Attributes:
        doc_title: Title of the document
        section_id: Section identifier (e.g., "1.2.3")
        title: Section title
        page: Page number where section starts
        level: Hierarchical level (computed from section_id)
        parent_id: Parent section ID (computed from section_id)
        full_path: Full path including section_id and title
    """
    doc_title: str = Field(description="Document title")
    section_id: str = Field(description="Section identifier (e.g., '1.2.3')")
    title: str = Field(description="Section title")
    page: int = Field(gt=0, description="Page number where section starts")
    level: int = Field(gt=0, description="Hierarchical level")
    parent_id: Optional[str] = Field(default=None, description="Parent section ID")
    full_path: str = Field(description="Full path with section_id and title")
    
    @field_validator("level", mode="before")
    @classmethod
    def infer_level(cls, v: Any, info: ValidationInfo) -> int:
        """Infer hierarchical level from section_id."""
        if v is not None:
            return int(v)
        section_id = str(info.data.get("section_id", ""))
        return len(section_id.split("."))
    
    @field_validator("parent_id", mode="before")
    @classmethod
    def infer_parent(cls, v: Any, info: ValidationInfo) -> Optional[str]:
        """Infer parent section ID from section_id."""
        if v is not None:
            return str(v)
        section_id = str(info.data.get("section_id", ""))
        return None if "." not in section_id else ".".join(section_id.split(".")[:-1])
