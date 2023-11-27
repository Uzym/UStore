from aiogram.filters import Filter
from aiogram.types import Message
from src.services import UserService
import logging

user_service = UserService()


class IsAdmin(Filter):

    def __init__(self, admin: bool):
        self.admin = admin

    async def __call__(self, message: Message):
        tg_id = str(message.from_user.id)
        users = await user_service.users(tg_id=tg_id)
        return len(users) > 0 and users[0].admin
