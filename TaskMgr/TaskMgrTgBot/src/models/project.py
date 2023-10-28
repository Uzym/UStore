from typing import List
from pydantic import BaseModel
from .domain import Link, Project


class RequestCreateProject(BaseModel):
    title: str
    description: str


class ResponseGetProjectDto(BaseModel):
    project: Project
    links: List[Link]
