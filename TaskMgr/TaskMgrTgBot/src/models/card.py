from typing import List
from pydantic import BaseModel
from .domain import Link, Card


class RequestCreateCard(BaseModel):
    title: str
    description: str
    due: str
    tags: List[str]


class ResponseGetCard(BaseModel):
    card: Card
    links: List[Link]
