import logging

from .store_api import StoreApiService
from src.models import domain, series
from typing import List, Optional
from pydantic.v1 import parse_obj_as, parse_raw_as
from json import loads


class SeriesService(StoreApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/series"

    async def get_series(self, series_id: int) -> domain.Series:
        url = self.api_key + self.controller + "/" + str(series_id)
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Series.parse_obj(data)

    async def create_series(self, title: str, description: Optional[str], firm_id: int,
                            discount: float = 1.0) -> domain.Series:
        url = self.api_key + self.controller
        request = loads(
            series.RequestCreateSeries(title=title, description=description, discount=discount, firm_id=firm_id).json(
                exclude_none=False))
        async with self.session.post(url, json=request) as response:
            data = await response.json()
            return domain.Series.parse_obj(data)

    async def series_list(self, title: Optional[str] = None, description: Optional[str] = None,
                          discount: Optional[float] = None, firm_id: Optional[int] = None,
                          category_id: Optional[int] = None) -> List[domain.Series]:
        url = self.api_key + self.controller
        params = {}
        if title is not None:
            params["title"] = title
        if description is not None:
            params["description"] = description
        if discount is not None:
            params["discount"] = discount
        if firm_id is not None:
            params["firm_id"] = firm_id
        if category_id is not None:
            params["category_id"] = category_id
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Series], data)

    async def update_series(self, series_id: int, title: Optional[str] = None, description: Optional[str] = None,
                            discount: Optional[float] = None, firm_id: Optional[int] = None) -> domain.Series:
        url = self.api_key + self.controller + f"/{series_id}/update"
        request = loads(
            series.RequestCreateSeries(title=title, description=description, discount=discount, firm_id=firm_id).json(
                exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Series.parse_obj(data)

    async def delete_series(self, series_id: int) -> bool:
        url = self.api_key + self.controller + f"/{series_id}/delete"
        async with self.session.delete(url) as response:
            if response.status == 200:
                data = await response.read()
                return parse_raw_as(bool, data)
