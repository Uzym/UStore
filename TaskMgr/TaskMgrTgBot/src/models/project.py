from typing import List, Optional
from pydantic import BaseModel
from .domain import Link, Project


class RequestCreateProject(BaseModel):
    title: Optional[str]
    description: Optional[str]


class ResponseGetProjectDto(BaseModel):
    project: Project
    links: List[Link]
