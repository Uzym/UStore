import logging

from .store_api import StoreApiService
from src.models import domain, user
from typing import List, Optional
from pydantic import parse_obj_as
from json import loads


class UserService(StoreApiService):

    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/user"

    async def get_user(self, user_id: int) -> domain.User:
        url = self.api_key + self.controller + "/" + str(user_id)
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.User.parse_obj(data)

    async def create_user(self, tg_id: str, name: str, adress: Optional[str], telephone: Optional[str],
                          email: Optional[str], tg_ref: Optional[str], admin: bool) -> domain.User:
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

    async def update_user(self, user_id: int, tg_id: Optional[str], name: Optional[str], adress: Optional[str],
                          telephone: Optional[str],
                          email: Optional[str], tg_ref: Optional[str], admin: Optional[bool]) -> domain.User:
        url = self.api_key + self.controller + f"/{user_id}/update"
        request = loads(user.RequestCreateUser(tg_id=tg_id, name=name, adress=adress, telephone=telephone, email=email,
                                               tg_ref=tg_ref, admin=admin).json(exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.User.parse_obj(data)
