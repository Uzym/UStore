from pydantic import BaseModel
from typing import List, Optional
from .domain import Card, Link


class ResponseGetCardDto(BaseModel):
    card: Card
    links: List[Link]

    def __str__(self):
        pass
