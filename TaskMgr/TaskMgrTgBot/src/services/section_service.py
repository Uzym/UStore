from logging import Logger

from .taskmgrapi import TaskMgrApiService
from .card_service import CardService
from src.models import section, domain, card
from typing import List
from pydantic import parse_obj_as
from json import loads


class SectionService(TaskMgrApiService):
    controller = "/section"

    def __init__(self, api_key: str, card_service: CardService, logger: Logger):
        super().__init__(api_key)
        self.card_service = card_service
        self.logger = logger

    async def get_section(self, section_id: int, telegram_id: str) -> domain.Section:
        url = self.api_key + self.controller + "/" + str(section_id)
        headers = {'Telegram-Id': telegram_id}
        async with self.session.get(url, headers=headers) as response:
            data = await response.json()
            return section.ResponseGetSection.parse_obj(data)

    async def update_section(self, section_id: int, title: str = None, project_id: int = None) -> domain.Section:
        request = loads(section.RequestCreateSection(title=title, project_id=project_id).json(exclude_none=True))
        url = self.api_key + self.controller + f"/{section_id}"
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Section.parse_obj(data)
            else:
                raise Exception

    async def cards(self, section_id: int, telegram_id: str) -> List[domain.Card]:
        url = self.api_key + self.controller + f"/{section_id}/card"

        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                cards = parse_obj_as(List[domain.Card], data)
                return cards
            else:
                raise Exception

    async def create_card(self, telegram_id, section_id, title):
        url = self.api_key + self.controller + f"/{section_id}/card"
        request = loads(card.RequestCreateCard(title=title, description=None, due=None, tags=[], section_id=None).json())
        headers = {'Telegram-Id': telegram_id}
        async with self.session.post(url, json=request, headers=headers) as response:
            data = await response.json()
            return domain.Card.parse_obj(data)
