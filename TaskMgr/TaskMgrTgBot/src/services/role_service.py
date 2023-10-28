import logging

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
