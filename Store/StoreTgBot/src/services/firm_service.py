import logging

from .store_api import StoreApiService
from src.models import domain, firm
from typing import List, Optional
from pydantic.v1 import parse_obj_as
from json import loads


class FirmService(StoreApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/firm"

    async def get_firm(self, firm_id: int) -> domain.Firm:
        url = self.api_key + self.controller + "/" + str(firm_id)
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Firm.parse_obj(data)

    async def create_firm(self, title: str, description: Optional[str], discount: float = 1.0) -> domain.Firm:
        url = self.api_key + self.controller
        request = loads(
            firm.RequestCreateFirm(title=title, description=description, discount=discount).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            data = await response.json()
            return domain.Firm.parse_obj(data)

    async def firms(self, title: Optional[str] = None, description: Optional[str] = None, discount: Optional[float] = None) \
            -> List[domain.Firm]:
        url = self.api_key + self.controller
        params = {}
        if title is not None:
            params["title"] = title
        if description is not None:
            params["description"] = description
        if discount is not None:
            params["discount"] = discount
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Firm], data)

    async def update_firm(self, firm_id: int, title: Optional[str], description: Optional[str],
                          discount: Optional[float]) -> domain.Firm:
        url = self.api_key + self.controller + f"/{firm_id}/update"
        request = loads(
            firm.RequestCreateFirm(title=title, description=description, discount=discount).json(exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Firm.parse_obj(data)