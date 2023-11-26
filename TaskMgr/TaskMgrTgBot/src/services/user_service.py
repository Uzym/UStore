from .taskmgrapi import TaskMgrApiService
from src.models import user, domain
from typing import List
from pydantic import parse_obj_as
from json import loads


class UserService(TaskMgrApiService):
    instance = None

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)

        return cls.instance

    def __init__(self, api_key: str = None):
        super().__init__(api_key=api_key)
        self.controller = "/user"

    async def get_user(self, user_id: int) -> domain.User:
        url = self.api_key + self.controller + "/" + str(user_id)
        async with self.session.get(url) as response:
            data = await response.json()
            return domain.User.parse_obj(data)

    async def create_user(self, name: str, telegram_id: str) -> domain.User:
        request = loads(user.RequestCreateUser(name=name, telegram_id=telegram_id).json())
        url = self.api_key + self.controller
        async with self.session.post(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.User.parse_obj(data)
            else:
                raise Exception

    async def users(self, telegram_id: str = None, name: str = None) -> List[domain.User]:
        url = self.api_key + self.controller
        params = {}
        if telegram_id is not None:
            params["telegram_id"] = telegram_id
        if name is not None:
            params["name"] = name

        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.User], data)
            else:
                raise Exception
