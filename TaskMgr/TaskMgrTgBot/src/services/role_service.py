import logging
from typing import List

from pydantic import parse_obj_as

from .taskmgrapi import TaskMgrApiService
from src.models import domain


class RoleService(TaskMgrApiService):
    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/role"

    async def get_role(self, role_id: int) -> domain.Role:
        url = self.api_key + self.controller + f"/{role_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Role.parse_obj(data)

    async def roles(self, title: str = None, description: str = None, table: str = None) -> list[domain.Role]:
        url = self.api_key + self.controller
        params = {}
        if title is not None:
            params["title"] = title
        if description is not None:
            params["description"] = description
        if table is not None:
            params["table"] = table

        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Role], data)
            else:
                raise Exception
