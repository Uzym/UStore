import logging

from .store_api import StoreApiService
from src.models import domain, user
from typing import List, Optional
from pydantic.v1 import parse_obj_as
from json import loads


class UserService(StoreApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/user"

    async def get_user(self, user_id: int) -> domain.User:
        url = self.api_key + self.controller + "/" + str(user_id)
        self.logger.info(url)
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                self.logger.info(data)
                return domain.User.parse_obj(data)

    async def create_user(self, tg_id: str, name: str, adress: Optional[str] = None, telephone: Optional[str] = None,
                          email: Optional[str] = None, tg_ref: Optional[str] = None, admin: bool = False) -> domain.User:
        url = self.api_key + self.controller
        request = loads(user.RequestCreateUser(tg_id=tg_id, name=name, adress=adress, telephone=telephone, email=email,
                                               tg_ref=tg_ref, admin=admin).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.User.parse_obj(data)

    async def users(self, tg_id: Optional[str]) -> List[domain.User]:
        url = self.api_key + self.controller
        params = {}
        if tg_id is not None:
            params["tg_id"] = tg_id
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.User], data)

    async def update_user(self, user_id: int, tg_id: Optional[str] = None, name: Optional[str] = None,
                          adress: Optional[str] = None, telephone: Optional[str] = None,
                          email: Optional[str] = None, tg_ref: Optional[str] = None,
                          admin: Optional[bool] = None) -> domain.User:
        url = self.api_key + self.controller + f"/{user_id}/update"
        request = loads(user.RequestCreateUser(tg_id=tg_id, name=name, adress=adress, telephone=telephone, email=email,
                                               tg_ref=tg_ref, admin=admin).json(exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.User.parse_obj(data)
