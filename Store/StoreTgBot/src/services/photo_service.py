import logging

from .store_api import StoreApiService
from src.models import domain, photo
from typing import List, Optional
from pydantic.v1 import parse_raw_as
from json import loads

from ..models.domain import Photo


class PhotoService(StoreApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/photo"

    async def get_photo(self, photo_id: int) -> domain.Photo:
        url = self.api_key + self.controller + f"/{photo_id}"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Photo.parse_obj(data)

    async def create_photo(self, name: str, product_id: int = None, category_id: int = None, series_id: int = None,
                           firm_id: int = None) -> domain.Photo:
        url = self.api_key + self.controller
        request = loads(
            photo.RequestCreatePhoto(name=name, product_id=product_id, category_id=category_id, series_id=series_id,
                                     firm_id=firm_id).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            data = await response.json()
            return domain.Photo.parse_obj(data)

    async def delete_photo(self, photo_id: int) -> bool:
        url = self.api_key + self.controller + f"/{photo_id}"
        async with self.session.delete(url) as response:
            data = await response.read()
            return parse_raw_as(bool, data)

    async def photos(self, product_id: Optional[int] = None, firm_id: Optional[str] = None,
                     series_id: Optional[str] = None, category_id: Optional[str] = None) -> List[Photo]:
        url = self.api_key + self.controller
        params = {}
        if product_id is not None:
            params["product_id"] = product_id
        if firm_id is not None:
            params["firm_id"] = firm_id
        if series_id is not None:
            params["series_id"] = series_id
        if category_id is not None:
            params["category_id"] = category_id
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.read()
                return parse_raw_as(List[Photo], data)
