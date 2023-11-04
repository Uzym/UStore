from typing import List

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const

from src.states.states import Main
from src.windows.main.window.to_main_menu_button import to_main_menu_button
from src.lexicon import LEXICON
from src.models import domain
from src.services import UserService

user_service = UserService()


async def get_me_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    try:
        users: List[domain.User] = await user_service.users(telegram_id=str(callback.from_user.id))
        manager.dialog_data['user_name'] = users[0].name
        manager.dialog_data['user_id'] = users[0].user_id
        await manager.switch_to(state=Main.get_me)
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


get_me_window = Window(
    Format("<i>{dialog_data[user_id]}</i> <b>{dialog_data[user_name]}</b>"),
    to_main_menu_button,
    state=Main.get_me,
)

get_me_button = Button(
    Const(LEXICON["get_me"]),
    id="get_me",
    on_click=get_me_button
)
