import logging
from typing import List

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const

from src.states.states import Main
from src.handlers.main.window.to_main_menu_button import to_main_menu_button
from src.lexicon import LEXICON
from src.models import domain
from src.services import UserService

from config import Config, load_config

config: Config = load_config()
logger = logging.getLogger()

user_service = UserService(api_key=config.api_key, logger=logger)


async def get_me_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    try:
        users = await user_service.users(tg_id=str(callback.from_user.id))
        logger.info(str(callback.from_user.id))
        logger.info(users)
        manager.dialog_data['user_name'] = users[0].name
        manager.dialog_data['user_id'] = users[0].user_id
        manager.dialog_data['user_address'] = users[0].adress
        manager.dialog_data['user_telephone'] = users[0].telephone
        manager.dialog_data['user_email'] = users[0].email
        manager.dialog_data['user_tg'] = users[0].tg_id
        await manager.switch_to(state=Main.get_me)
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


get_me_window = Window(
    Format('Уникальный номер: {dialog_data[user_id]}\n'
           'Имя: {dialog_data[user_name]}\n'
           'Адрес: {dialog_data[user_address]}\n'
           'Телефон: {dialog_data[user_telephone]}\n'
           'Email: {dialog_data[user_email]}\n'
           'Telegram Id: {dialog_data[user_tg]}'),
    to_main_menu_button,
    state=Main.get_me,
)

get_me_button = Button(
    Const(LEXICON["get_me"]),
    id="get_me",
    on_click=get_me_button
)