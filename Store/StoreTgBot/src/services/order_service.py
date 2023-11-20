import logging

from .store_api import StoreApiService
from src.models import domain, order, card
from typing import List, Optional
from pydantic import parse_obj_as
from pydantic.v1 import parse_raw_as
from json import loads


class OrderService(StoreApiService):

    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger = logger
        self.controller = "/order"

    async def get_order(self, tg_id: str, order_id: int) -> domain.Order:
        url = self.api_key + self.controller + f"/{order_id}"
        params = {
            "tg_id": tg_id
        }
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Order.parse_obj(data)

    async def create_order(self, tg_id: str) -> domain.Order:
        url = self.api_key + self.controller
        params = {
            "tg_id": tg_id
        }
        request = loads(order.RequestCreateOrder(user_id=0, card_id=0, finished=False, price=0).json())
        async with self.session.post(url, params=params, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Order.parse_obj(data)

    async def orders(self, tg_id: str, finished: Optional[bool]) -> List[domain.Order]:
        url = self.api_key + self.controller
        params = {
            "tg_id": tg_id
        }
        if finished is not None:
            params["finished"] = finished
        async with self.session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.Order], data)

    async def delete_order(self, tg_id: str, order_id: int) -> bool:
        url = self.api_key + self.controller + f"/{order_id}"
        params = {
            "tg_id": tg_id
        }
        async with self.session.delete(url, params=params) as response:
            data = await response.read()
            return parse_raw_as(bool, data)

    async def order_products(self, tg_id: str, order_id: int) -> List[order.OrderProduct]:
        url = self.api_key + self.controller + f"/{order_id}/products"
        params = {
            "tg_id": tg_id
        }
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            return parse_obj_as(List[order.OrderProduct], data)

    async def add_order_product(self, tg_id: str, order_id: int, product_id: int,
                                quantity: int = 1) -> order.OrderProduct:
        url = self.api_key + self.controller + f"/{order_id}/products"
        params = {
            "tg_id": tg_id
        }
        request = loads(
            order.OrderProduct(order_id=order_id, product_id=product_id, quantity=quantity).json(exclude_none=False))
        async with self.session.post(url, params=params, json=request) as response:
            data = await response.json()
            return order.OrderProduct.parse_obj(data)

    async def delete_order_product(self, tg_id: str, order_id: int, product_id: int) -> domain.Order:
        url = self.api_key + self.controller + f"/{order_id}/product/{product_id}/delete"
        params = {
            "tg_id": tg_id
        }
        async with self.session.patch(url, params=params) as response:
            data = await response.json()
            return domain.Order.parse_obj(data)

    async def confirm_order(self, tg_id: str, order_id: int, section_id: int) -> card.ResponseGetCardDto:
        url = self.api_key + self.controller + f"/{order_id}/confirm"
        params = {
            "tg_id": tg_id,
            "section_id": section_id
        }
        async with self.session.patch(url, params=params) as response:
            data = await response.json()
            return card.ResponseGetCardDto.parse_obj(data)

    async def order_card(self, tg_id: str, order_id: int) -> card.ResponseGetCardDto:
        url = self.api_key + self.controller + f"/{order_id}/card"
        params = {
            "tg_id": tg_id
        }
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            return card.ResponseGetCardDto.parse_obj(data)
