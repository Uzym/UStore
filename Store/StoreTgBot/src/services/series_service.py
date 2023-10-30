import logging

from .store_api import StoreApiService
from src.models import domain, series
from typing import List, Optional
from pydantic import parse_obj_as
from json import loads


class SeriesService(StoreApiService):

    def __init__(self, api_key: str, logger: logging.Logger):
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

    async def series_list(self, title: Optional[str], description: Optional[str], discount: Optional[float],
                          firm_id: Optional[int]) -> List[domain.Series]:
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
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Series], data)

    async def update_series(self, series_id: int, title: Optional[str], description: Optional[str],
                            discount: Optional[float], firm_id: Optional[int]) -> domain.Series:
        url = self.api_key + self.controller + f"/{series_id}/update"
        request = loads(
            series.RequestCreateSeries(title=title, description=description, discount=discount, firm_id=firm_id).json(
                exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Series.parse_obj(data)
