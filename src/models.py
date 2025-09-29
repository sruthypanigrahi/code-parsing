from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, ValidationInfo, field_validator


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
        full_path: Full path including section_id and title
        page: Page number where section starts
        level: Hierarchical level (computed from section_id)
        parent_id: Parent section ID (computed from section_id)
        tags: Additional tags for categorization
    """

    doc_title: str = Field(description="Document title")
    section_id: str = Field(description="Section identifier (e.g., '1.2.3')")

    @field_validator("section_id")
    @classmethod
    def validate_section_id(cls, v: str) -> str:
        """Validate section_id format for proper hierarchy."""
        if not v or not v.strip():
            raise ValueError("section_id cannot be empty")

        # Allow alphanumeric sections with dots (e.g., "1.2.3", "A.1", "1")
        import re

        if not re.match(r"^[A-Za-z0-9]+(?:\.[A-Za-z0-9]+)*$", v.strip()):
            raise ValueError(f"Invalid section_id format: {v}")

        return v.strip()

    title: str = Field(description="Section title")
    full_path: str = Field(description="Full path with section_id and title")
    page: int = Field(gt=0, description="Page number where section starts")
    level: int = Field(gt=0, description="Hierarchical level")
    parent_id: Optional[str] = Field(default=None, description="Parent section ID")
    tags: list[str] = Field(default_factory=list, description="Additional tags")

    @field_validator("level", mode="before")
    @classmethod
    def infer_level(cls, v: Any, info: ValidationInfo) -> int:
        """Infer hierarchical level from section_id."""
        if v is not None:
            try:
                return int(v)
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid level value: {v}") from e
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


class ContentItem(BaseModel):
    """Represents a content item extracted from PDF (paragraph, image, table)."""

    doc_title: str = Field(description="Document title")
    content_id: str = Field(description="Unique content identifier")
    type: str = Field(description="Content type: paragraph, image, table")
    content: str = Field(description="Content text or description")
    page: int = Field(gt=0, description="Page number")
    block_id: str = Field(description="Block identifier")
    bbox: List[float] = Field(
        default_factory=list, description="Bounding box coordinates"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict, description="Additional metadata"
    )
