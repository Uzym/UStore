from typing import List
from pydantic import BaseModel
from .domen import Link, Card


class RequestCreateUser(BaseModel):
    name: str
    telegram_id: str


class ResponseGetCard(BaseModel):
    card: Card
    links: List[Link]
