import logging

from .taskmgrapi import TaskMgrApiService
from src.models import project, domain, section
from typing import List
from pydantic import parse_obj_as
from json import loads


def parse_link_project(link: domain.Link):
    url = link.href.lower().split('/')
    if url[1].lower() != "project":
        raise Exception
    project_id: int = int(url[2])
    if len(url) == 3:
        if link.method == "PUT":
            return project_id, "update"
        if link.method == "GET":
            return project_id, "get"
    if len(url) == 4:
        if link.method == "POST" and url[3] == "section":
            return project_id, "add_section"
        if link.method == "GET" and url[3] == "section":
            return project_id, "get_section"
        if link.method == "POST" and url[3] == "user":
            return project_id, "add_user"
        if link.method == "GET" and url[3] == "user":
            return project_id, "get_user"
    return project_id, "post"


class ProjectService(TaskMgrApiService):
    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/project"

    async def get_project(self, project_id: int, telegram_id: str = None) -> project.ResponseGetProjectDto:
        headers = {
            'Telegram-Id': telegram_id
        }
        url = self.api_key + self.controller + "/" + str(project_id)
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return project.ResponseGetProjectDto.parse_obj(data)
            else:
                raise Exception

    async def create_project(self, title: str, description: str = None) -> domain.Project:
        url = self.api_key + self.controller
        request = loads(project.RequestCreateProject(title=title, description=description).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Project.parse_obj(data)
            else:
                raise Exception

    async def update_project(self, project_id: int, title: str = None, description: str = None) -> domain.Project:
        url = self.api_key + self.controller + "/" + str(project_id)
        request = loads(project.RequestCreateProject(title=title, description=description).json(exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Project.parse_obj(data)

    async def projects(self, telegram_id: str = None) -> List[domain.Project]:
        headers = {
            "Telegram-Id": telegram_id
        }
        url = self.api_key + self.controller
        async with self.session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Project], data)

    async def add_user_to_project(self, project_id: int, user_id: int, role_id: int) -> List[domain.AddUser]:
        url = self.api_key + self.controller + "/" + str(project_id) + "/user"
        request = loads(domain.AddUser(user_id=user_id, role_id=role_id).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.AddUser], data)

    async def get_users(self, project_id: int) -> List[domain.AddUser]:
        url = self.api_key + self.controller + "/" + str(project_id) + "/user"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.AddUser], data)

    async def add_section_to_project(self, project_id: int, title: str) -> domain.Section:
        url = self.api_key + self.controller + "/" + str(project_id) + "/section"
        request = loads(section.RequestCreateSection(title=title, project_id=project_id).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Section.parse_obj(data)

    async def get_sections(self, project_id: int) -> List[domain.Section]:
        url = self.api_key + self.controller + "/" + str(project_id) + "/section"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Section], data)