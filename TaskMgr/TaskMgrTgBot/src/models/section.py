from typing import List
from pydantic import BaseModel
from .domen import Link, Section


class RequestCreateSection(BaseModel):
    title: str


class ResponseGetSection(BaseModel):
    section: Section
    links: List[Link]
