from logging import Logger

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, and_f
from aiogram_dialog import DialogManager, StartMode
from typing import List

from src.services import UserService, SectionService
from src.lexicon import LEXICON
from src.models import domain
from src.states.states import Main


router: Router = Router()





# @router.message(Command(commands=["me"]))
# async def get_me(message: Message, user_service: UserService):
#     try:
#         users: List[domain.User] = await user_service.users(telegram_id=str(message.from_user.id))
#         await message.answer(text=str(users[0]))
#     except:
#         await message.answer(text=LEXICON["not_found"])
#
#
# @router.message(Command(commands=["skip"]))
# async def skip(
#         message: Message,
#         state: FSMContext
# ):
#     try:
#         await state.clear()
#         await message.answer(text=LEXICON["skip"])
#     except:
#         await message.answer(text=LEXICON["not_found"])
#
#
# @router.callback_query(FormCallback.filter(F.cnt > 0))
# async def get_user_input_start(
#         callback: CallbackQuery,
#         callback_data: FormCallback,
#         state: FSMContext,
# ):
#     await callback.answer(text=LEXICON["loading"])
#     try:
#         await state.clear()
#         await state.set_state(DefualtForm.user_input)
#         await state.set_data({"cnt": callback_data.cnt, "input": []})
#         await callback.message.answer(text=f"{callback_data.obj} {callback_data.tag} {callback_data.cnt}")
#     except:
#         await callback.answer(text=LEXICON["not_found"])
#

# @router.message(DefualtForm.user_input)
# async def get_user_input(
#         message: Message,
#         state: FSMContext
# ):
#     try:
#         data = await state.get_data()
#         data["input"].append(message.text)
#         data["cnt"] = data["cnt"] - 1
#     except:
#         await message.answer(text=LEXICON["not_found"])
