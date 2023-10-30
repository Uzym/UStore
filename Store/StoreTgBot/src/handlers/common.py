from logging import Logger

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from src.lexicon import LEXICON
from aiogram.filters import Command
from typing import List

router: Router = Router()

@router.message(Command(commands=["start"]))
async def start_message(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["start"])