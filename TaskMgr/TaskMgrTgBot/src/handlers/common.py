from logging import Logger

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from typing import List

from src.services import UserService, SectionService
from src.lexicon import LEXICON
from src.models import domain


router: Router = Router()


@router.message(Command(commands=["start"]))
async def start_message(message: Message, user_service: UserService, state: FSMContext):
    user: domain.User = await user_service.create_user(name=message.from_user.full_name,
                                                       telegram_id=str(message.from_user.id))
    await state.update_data(user_id=user.user_id)
    await message.answer(text=LEXICON["start"])


@router.message(Command(commands=["help"]))
async def help_message(message: Message, section_service: SectionService, logger: Logger):
    a = await section_service.get_section(telegram_id=str(message.from_user.id), section_id=1)
    logger.info(str(a))
    b = await section_service.update_section(section_id=1, title="Залупа слоника", project_id=1)
    logger.info(str(b))
    c = await section_service.cards(telegram_id=str(message.from_user.id), section_id=1)
    logger.info(str(c))
    d = await section_service.create_card(telegram_id=str(message.from_user.id), section_id=1, title="BOBOB")
    logger.info(str(d))

    await message.answer(text=LEXICON["help"])


@router.message(Command(commands=["me"]))
async def get_me(message: Message, user_service: UserService):
    users: List[domain.User] = await user_service.users(telegram_id=str(message.from_user.id))
    if len(users) == 0:
        await message.answer(text=LEXICON["not_found_user"])
    else:
        await message.answer(text=str(users[0]))
