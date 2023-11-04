import logging

from .taskmgrapi import TaskMgrApiService
from src.models import card, domain
from typing import List
from pydantic import parse_obj_as
from json import loads


def parse_link_card(link: domain.Link):
    url = link.href.lower().split('/')
    if url[1].lower() != "card":
        raise Exception
    card_id: int = int(url[2])
    if len(url) == 3:
        if link.method == "PUT":
            return card_id, "update"
        if link.method == "GET":
            return card_id, "get"
    if len(url) == 4:
        if link.method == "PATCH" and url[3] == "uncomplete":
            return card_id, "uncomplete"
        if link.method == "PATCH" and url[3] == "complete":
            return card_id, "complete"
        if link.method == "POST" and url[3] == "comment":
            return card_id, "add_comment"
        if link.method == "GET" and url[3] == "comment":
            return card_id, "get_comment"
        if link.method == "POST" and url[3] == "user":
            return card_id, "add_user"
        if link.method == "GET" and url[3] == "user":
            return card_id, "get_user"
    return card_id, "post"


class CardService(TaskMgrApiService):
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)

        return cls.__instance

    controller = "/card"

    def __init__(self, api_key: str = None, logger: logging.Logger = None):
        super().__init__(api_key=api_key)
        self.logger = logger

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
        request = loads(card.RequestCreateComment(description=description).json())
        headers = {'Telegram-Id': telegram_id}
        async with self.session.post(url, json=request, headers=headers) as response:
            data = await response.json()
            return domain.Comment.parse_obj(data)


    async def update_card(self,
                          card_id: int,
                          title: str = None,
                          description: str = None,
                          due: str = None,
                          tags: List[str] = None,
                          section_id: int = None) -> domain.Card:
        url = self.api_key + self.controller + "/" + str(card_id)
        request = loads(card.RequestCreateCard(
            title=title,
            description=description,
            due=due,
            tags=tags,
            section_id=section_id).json(exclude_none=False))
        async with self.session.put(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Card.parse_obj(data)

    async def add_user(self, card_id: int, user_id: int, role_id: int) -> List[domain.AddUser]:
        url = self.api_key + self.controller + f"/{card_id}/user"
        request = loads(domain.AddUser(user_id=user_id, role_id=role_id).json(exclude_none=False))
        async with self.session.post(url, json=request) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.AddUser], data)

    async def get_users(self, card_id: int) -> List[domain.AddUser]:
        url = self.api_key + self.controller + f"/{card_id}/user"
        async with self.session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return parse_obj_as(List[domain.AddUser], data)

    async def complete_card(self, card_id: int) -> domain.Card:
        url = self.api_key + self.controller + f"/{card_id}/complete"
        async with self.session.patch(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Card.parse_obj(data)

    async def uncomplete_card(self, card_id: int) -> domain.Card:
        url = self.api_key + self.controller + f"/{card_id}/uncomplete"
        async with self.session.patch(url) as response:
            if response.status == 200:
                data = await response.json()
                return domain.Card.parse_obj(data)