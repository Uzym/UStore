from typing import List, Optional
from pydantic import BaseModel
from .domain import Link, Card


class RequestCreateCard(BaseModel):
    title: Optional[str]
    description: Optional[str]
    due: Optional[str]
    tags: Optional[List[str]]
    section_id: Optional[int]


class ResponseGetCard(BaseModel):
    card: Card
    links: List[Link]


class RequestCreateComment(BaseModel):
    description: str
