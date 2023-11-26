import logging

from .store_api import StoreApiService
from src.models import domain, order, card, comment
from typing import List, Optional
from pydantic.v1 import parse_obj_as
from pydantic.v1 import parse_raw_as
from json import loads


class OrderService(StoreApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
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

    async def orders(self, tg_id: str, finished: Optional[bool] = None) -> List[domain.Order]:
        url = self.api_key + self.controller
        params = {
            "tg_id": tg_id
        }
        if finished is not None:
            params["finished"] = "true" if finished else "false"
        self.logger.info(params)
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

    async def confirm_order(self, tg_id: str, order_id: int) -> domain.Card:
        url = self.api_key + self.controller + f"/{order_id}/confirm"
        params = {
            "tg_id": tg_id
        }
        async with self.session.patch(url, params=params) as response:
            data = await response.json()
            self.logger.info(data)
            # return card.ResponseGetCardDto.parse_obj(data)
            return domain.Card.parse_obj(data)

    async def order_card(self, tg_id: str, order_id: int) -> card.ResponseGetCardDto:
        url = self.api_key + self.controller + f"/{order_id}/card"
        params = {
            "tg_id": tg_id
        }
        async with self.session.get(url, params=params) as response:
            data = await response.json()
            return card.ResponseGetCardDto.parse_obj(data)

    async def order_comments(self, order_id: int) -> List[domain.Comment]:
        url = self.api_key + self.controller + f"/{order_id}/comments"
        async with self.session.get(url) as response:
            data = await response.json()
            return parse_obj_as(List[domain.Comment], data)

    async def add_comment(self, order_id: str, description: str) -> None:
        url = self.api_key + self.controller + f"/{order_id}/comments"
        request = loads(
            comment.RequestCreateCommentDto(description=description).json(exclude_none=False))
        async with self.session.post(url=url, json=request) as response:
            data = await response.json()
            return None
