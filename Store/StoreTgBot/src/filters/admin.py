from aiogram.filters import Filter
from aiogram.types import Message
from src.services import UserService


class IsAdmin(Filter):
    async def check(self, message: Message, user_service: UserService):
        tg_id = str(message.from_user.id)
        users = await user_service.users(tg_id=tg_id)
        return len(users) > 0
