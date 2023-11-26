import logging

from .store_api import StoreApiService
from src.models import domain, category
from typing import List, Optional
from pydantic.v1 import parse_obj_as, parse_raw_as
from json import loads


class CategoryService(StoreApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/category"

    async def get_category(self, category_id: int) -> domain.Category:
        url = self.api_key + self.controller + "/" + str(category_id)
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Category.parse_obj(data)

    async def create_category(self, title: str, description: Optional[str], discount: float = 1.0) -> domain.Category:
        url = self.api_key + self.controller
        request = loads(
            category.RequestCreateCategory(title=title, description=description, discount=discount).json(
                exclude_none=False))
        async with self.session.post(url, json=request) as response:
            data = await response.json()
            return domain.Category.parse_obj(data)

    async def categories(self, title: Optional[str] = None, description: Optional[str] = None,
                         discount: Optional[float] = None) -> List[domain.Category]:
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
                return parse_obj_as(List[domain.Category], data)

    async def update_category(self, category_id: int, title: Optional[str], description: Optional[str],
                              discount: Optional[float]) -> domain.Category:
        url = self.api_key + self.controller + f"/{category_id}/update"
        request = loads(
            category.RequestCreateCategory(title=title, description=description, discount=discount).json(
                exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Category.parse_obj(data)

    async def delete_category(self, category_id: int) -> bool:
        url = self.api_key + self.controller + f"/{category_id}/delete"
        async with self.session.delete(url) as response:
            if response.status == 200:
                data = await response.read()
                return parse_raw_as(bool, data)
