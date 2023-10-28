from typing import List
from pydantic import BaseModel
from .domain import Link, Section


class RequestCreateSection(BaseModel):
    title: str | None
    project_id: int | None


class ResponseGetSection(BaseModel):
    section: Section
    links: List[Link]
