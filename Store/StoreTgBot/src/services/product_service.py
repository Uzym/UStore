import logging

from .store_api import StoreApiService
from src.models import domain, product
from typing import List, Optional
from pydantic import parse_obj_as
from json import loads


class ProductService(StoreApiService):

    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/product"

    async def get_product(self, product_id: int) -> domain.Product:
        url = self.api_key + self.controller + f"/{product_id}"
        async with self.session.get(url) as response:
            data = await response.json()
            return domain.Product.parse_obj(data)

    async def create_product(self, category_id: int, series_id: Optional[int], title: str, description: Optional[str],
                             cost: float, delivery_time: str, discount: float = 1.0) -> domain.Product:
        url = self.api_key + self.controller
        request = loads(product.RequestCreateProduct(category_id=category_id, series_id=series_id, title=title,
                                                     description=description, cost=cost, delivery_time=delivery_time,
                                                     discount=discount).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Product.parse_obj(data)

    async def update_product(self, product_id: Optional[int], category_id: Optional[int], series_id: Optional[int],
                             title: Optional[str], description: Optional[str],
                             cost: Optional[float], delivery_time: Optional[str],
                             discount: Optional[float]) -> domain.Product:
        url = self.api_key + self.controller + f"/{product_id}/update"
        request = loads(product.RequestCreateProduct(category_id=category_id, series_id=series_id, title=title,
                                                     description=description, cost=cost, delivery_time=delivery_time,
                                                     discount=discount).json(exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Product.parse_obj(data)

    async def products(self, category_id: Optional[int], series_id: Optional[int], title: Optional[str],
                       description: Optional[str],
                       cost: Optional[float], delivery_time: Optional[str],
                       discount: Optional[float]) -> List[domain.Product]:
        url = self.api_key + self.controller
        params = {}
        if category_id is not None:
            params["category_id"] = category_id
        if series_id is not None:
            params["series_id"] = series_id
        if title is not None:
            params["title"] = title
        if description is not None:
            params["description"] = description
        if cost is not None:
            params["cost"] = cost
        if delivery_time is not None:
            params["delivery_time"] = delivery_time
        if discount is not None:
            params["discount"] = discount
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Product], data)
