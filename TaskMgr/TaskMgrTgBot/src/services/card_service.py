import logging

from .taskmgrapi import TaskMgrApiService
from src.models import card, domain
from typing import List
from pydantic import parse_obj_as
from json import loads


class CardService(TaskMgrApiService):
    controller = "/card"

    def __init__(self, api_key: str, logger: logging.Logger):
        super().__init__(api_key=api_key)
        self.logger=logger

    async def get_card(self, card_id: int, telegram_id: str) -> card.ResponseGetCard:
        url = self.api_key + self.controller + "/" + str(card_id)
        headers = {'Telegram-Id': telegram_id}
        async with self.session.get(url, headers=headers) as response:
            data = await response.json()
            return card.ResponseGetCard.parse_obj(data)

    async def comments(self, card_id: int) -> List[domain.Comment]:
        url = self.api_key + self.controller + f"/{card_id}/comment"
        async with self.session.get(url) as response:
            data = await response.json()
            return parse_obj_as(List[domain.Comment], data)

    async def create_comment(self, telegram_id: str, card_id: int, description: str) -> domain.Comment:
        url = self.api_key + self.controller + f"/{card_id}/comment"
        request = loads(card.RequestCreateCard(description=description).json())
        headers = {'Telegram-Id': telegram_id}
        async with self.session.post(url, json=request, headers=headers) as response:
            data = await response.json()
            return domain.Comment.parse_obj(data)



