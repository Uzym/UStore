from logging import Logger

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.services import UserService
from src.lexicon import LEXICON

router: Router = Router()

@router.message(Command(commands=["start"]))
async def start_message(message: Message, user_service: UserService, logger: Logger):
    # logger.info(str(await user_service.get_user(1)))
    # logger.info(str(await user_service.users()))
    logger.info(str(await user_service.create_user(name=message.from_user.full_name, telegram_id=str(message.from_user.id))))
    await message.answer(text=LEXICON["start"])

@router.message(Command(commands=["help"]))
async def help_message(message: Message):
    await message.answer(text=LEXICON["help"])

@router.message(Command(commands=["me"]))
async def get_me(message: Message):
    pass

@router.message()
async def process_any_message(message: Message):
    await message.reply(text=message.text)