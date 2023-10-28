from .taskmgrapi import TaskMgrApiService
from src.models import card, domain
from typing import List
from pydantic import parse_obj_as
from json import loads


class CardService(TaskMgrApiService):
    controller = "/card"

    # def __init__(self, api_key: str, card_service: CardService):

    async def get_card(self, card_id: int, telegram_id: str) -> card.ResponseGetCard:
        url = self.api_key + self.controller + "/" + str(card_id)
        headers = {'Telegram-Id': telegram_id}
        async with self.session.get(url, headers=headers) as response:
            data = await response.json()
            return card.ResponseGetCard.parse_obj(data)

