import logging
from typing import List

from aiogram import html
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.input import MessageInput
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


async def user_update_go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Main.get_me)


user_update_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="user_update_go_back",
    on_click=user_update_go_back_button
)


async def user_update_address_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Main.update_address)


async def user_update_address(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    user = await user_service.users(tg_id=str(dialog_manager.event.from_user.id))
    await user_service.update_user(user_id=user[0].user_id,
                                   tg_id=str(dialog_manager.event.from_user.id),
                                   adress=message.text)
    await dialog_manager.switch_to(Main.get_me)


user_update_address_button = Button(
    text=Const("Изменить адрес"),
    id="user_update_address",
    on_click=user_update_address_button
)

user_update_address_window = Window(
    Const("Введите адрес"),
    MessageInput(user_update_address),
    user_update_go_back_button,
    state=Main.update_address
)


async def user_update_email_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Main.update_email)


async def user_update_email(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    user = await user_service.users(tg_id=str(dialog_manager.event.from_user.id))
    await user_service.update_user(user_id=user[0].user_id,
                                   tg_id=str(dialog_manager.event.from_user.id),
                                   email=message.text)
    await dialog_manager.switch_to(Main.get_me)


user_update_email_button = Button(
    text=Const("Изменить email"),
    id="user_update_email",
    on_click=user_update_email_button
)

user_update_email_window = Window(
    Const("Введите email"),
    MessageInput(user_update_email),
    user_update_go_back_button,
    state=Main.update_email
)


async def user_update_telephone_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Main.update_telephone)


async def user_update_telephone(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    user = await user_service.users(tg_id=str(dialog_manager.event.from_user.id))
    await user_service.update_user(user_id=user[0].user_id, tg_id=str(dialog_manager.event.from_user.id),
                                   telephone=message.text)
    await dialog_manager.switch_to(Main.get_me)


user_update_telephone_button = Button(
    text=Const("Изменить телефон"),
    id="user_update_telephone",
    on_click=user_update_telephone_button
)

user_update_telephone_window = Window(
    Const("Введите телефон"),
    MessageInput(user_update_telephone),
    user_update_go_back_button,
    state=Main.update_telephone
)


async def get_me_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    try:
        users = await user_service.users(tg_id=str(callback.from_user.id))
        # manager.dialog_data['user_name'] = users[0].name
        manager.dialog_data['user_id'] = users[0].user_id
        # manager.dialog_data['user_address'] = users[0].adress
        # manager.dialog_data['user_telephone'] = users[0].telephone
        # manager.dialog_data['user_email'] = users[0].email
        # manager.dialog_data['user_tg'] = users[0].tg_id
        await manager.switch_to(state=Main.get_me)
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


async def getter(dialog_manager: DialogManager, **kwargs):
    user_id = int(dialog_manager.dialog_data['user_id'])
    user_data = await user_service.get_user(user_id=user_id)
    return {
        "user_id": user_data.user_id,
        "user_name": user_data.name,
        "user_address": user_data.adress,
        "user_telephone": user_data.telephone,
        "user_email": user_data.email,
        "user_tg_id": user_data.tg_id
    }


get_me_window = Window(
    Format(html.bold(html.quote("Уникальный номер: {user_id}"))),
    Format(html.quote("Telegram Id: {user_tg_id}")),
    Format(html.quote("Имя: {user_name}")),
    Format(html.quote("Email: {user_email}")),
    Format(html.quote("Телефон: {user_telephone}")),
    Format(html.quote("Адрес: {user_address}")),
    user_update_telephone_button,
    user_update_email_button,
    user_update_address_button,
    to_main_menu_button,
    state=Main.get_me,
    getter=getter
)

get_me_button = Button(
    Const(LEXICON["get_me"]),
    id="get_me",
    on_click=get_me_button
)

