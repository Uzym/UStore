from typing import List, Optional
from pydantic import BaseModel
from .domain import Link, Section


class RequestCreateSection(BaseModel):
    title: Optional[str]
    project_id: Optional[int]


class ResponseGetSection(BaseModel):
    section: Section
    links: List[Link]
