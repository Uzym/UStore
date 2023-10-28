from typing import List

from pydantic import BaseModel


class Card(BaseModel):
    card_id: int
    title: str
    description: str
    due: str
    complete: str
    tags: List[str]
    created: str
    section_id: int


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


class User(BaseModel):
    user_id: int
    name: str
    telegram_id: str


class Project(BaseModel):
    project_id: int
    title: str
    description: str


class AddUser(BaseModel):
    user_id: int
    role_id: int


class Right(BaseModel):
    right_id: int
    title: str


class Role(BaseModel):
    role_id: int
    title: str
    description: str
    rights: List[Right]
