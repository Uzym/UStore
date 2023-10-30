from typing import List, Optional
from aiogram import html
from pydantic import BaseModel


class Card(BaseModel):
    card_id: Optional[int]
    title: Optional[str]
    description: Optional[str]
    due: Optional[str]
    complete: Optional[str]
    tags: Optional[List[str]]
    created: Optional[str]
    section_id: Optional[int]


class Link(BaseModel):
    href: str
    rel: str
    method: str


class Comment(BaseModel):
    description: str
    user_id: int


class Section(BaseModel):
    section_id: int
    title: str
    project_id: int

    def __str__(self):
        return f"{html.bold(self.title)}"


class User(BaseModel):
    user_id: int
    name: str
    telegram_id: str

    def __str__(self):
        return f"Имя: {html.bold(self.name)}\nID: {html.bold(self.user_id)}\nTelegramID: {html.bold(self.telegram_id)}"


class Project(BaseModel):
    project_id: int
    title: str
    description: str

    def __str__(self):
        return f"{html.italic(self.project_id)}: {html.bold(html.quote(self.title))}\n\n{html.quote(self.description)}"


class AddUser(BaseModel):
    user_id: int
    role_id: int

    def __str__(self):
        return f"{self.user_id} {self.role_id}"


class Right(BaseModel):
    right_id: int
    title: str


class Role(BaseModel):
    role_id: int
    title: str
    description: str
    rights: List[Right]
