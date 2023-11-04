from typing import List, Optional
from pydantic import BaseModel
from .domain import Link, Section


class RequestCreateSection(BaseModel):
    title: Optional[str] = None
    project_id: Optional[int] = None


class ResponseGetSection(BaseModel):
    section: Section
    links: List[Link]
