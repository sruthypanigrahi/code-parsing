from typing import  Optional, Any, Dict
from pydantic import BaseModel, validator

class PageContent(BaseModel):
    page: int
    text: str
    image_count: int
    table_count: int

class TOCEntry(BaseModel):
    doc_title: str
    section_id: str
    title: str
    page: int
    level: int
    parent_id: Optional[str] = None
    full_path: str

    @validator("level", pre=True, always=True)
    def infer_level(cls, v: Any, values: Dict[str, Any]) -> int:
        return len(str(values["section_id"]).split(".")) if v is None else int(v)

    @validator("parent_id", pre=True, always=True)
    def infer_parent(cls, v: Any, values: Dict[str, Any]) -> Optional[str]:
        if v is not None:
            return str(v)
        sid = str(values.get("section_id", ""))
        return None if "." not in sid else ".".join(sid.split(".")[:-1])
