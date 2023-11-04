from logging import Logger

from .taskmgrapi import TaskMgrApiService
from .card_service import CardService
from src.models import section, domain, card
from typing import List
from pydantic import parse_obj_as
from json import loads


def parse_link_section(link: domain.Link):
    url = link.href.lower().split('/')
    if url[1].lower() != "section":
        raise Exception
    section_id: int = int(url[2])
    if len(url) == 3:
        if link.method == "PUT":
            return section_id, "update"
        if link.method == "GET":
            return section_id, "get"
    if len(url) == 4:
        if link.method == "POST" and url[3] == "card":
            return section_id, "add_card"
        if link.method == "GET" and url[3] == "card":
            return section_id, "get_card"
    return section_id, "post"


class SectionService(TaskMgrApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    def __init__(self, api_key: str = None, card_service: CardService = None, logger: Logger = None):
        super().__init__(api_key)
        self.card_service = card_service
        self.logger = logger
        self.controller = "/section"

    async def get_section(self, section_id: int, telegram_id: str) -> section.ResponseGetSection:
        url = self.api_key + self.controller + "/" + str(section_id)
        headers = {'Telegram-Id': telegram_id}
        async with self.session.get(url, headers=headers) as response:
            data = await response.json()
            return section.ResponseGetSection.model_validate(data)

    async def update_section(self, section_id: int, title: str = None, project_id: int = None) -> domain.Section:
        request = loads(section.RequestCreateSection(title=title, project_id=project_id).json(exclude_none=False))
        url = self.api_key + self.controller + f"/{section_id}"
        async with self.session.put(url, json=request) as response:
            data = await response.json()
            return domain.Section.parse_obj(data)

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
        request = loads(card.RequestCreateCard(title=title, description=None, due=None, tags=[], section_id=section_id).json(exclude_none=False))
        headers = {'Telegram-Id': telegram_id}
        async with self.session.post(url, json=request, headers=headers) as response:
            data = await response.json()
            return domain.Card.parse_obj(data)
