import operator
import logging
from typing import Any
from aiogram import html
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import UserService
from src.states.states import User

user_service = UserService()
logger = logging.getLogger()


async def go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(User.users)


go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="go_back",
    on_click=go_back_button
)


async def tg_id_filter_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(User.users_search_tg_id_filter)


async def tg_id_filter(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data["tg_id"] = message.text
    await dialog_manager.switch_to(User.users_search)


tg_id_filter_button = Button(
    text=Const("Задать Telegram Id"),
    id="tg_id_filter",
    on_click=tg_id_filter_button
)

tg_id_filter_window = Window(
    Const("Введите Telegram Id"),
    MessageInput(tg_id_filter),
    Row(go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=User.users_search_tg_id_filter
)


async def users_search(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(User.users)


users_search_button = Button(
    text=Const(LEXICON["ok"]),
    id="users_search",
    on_click=users_search
)


users_search_window = Window(
    Const("Поиск людей"),
    Group(
        tg_id_filter_button,
        users_search_button,
        go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=User.users_search
)


async def users_getter(dialog_manager: DialogManager, **kwargs):
    tg_id = None
    if 'tg_id' in dialog_manager.dialog_data.keys():
        tg_id = dialog_manager.dialog_data['tg_id']
    users_data = await user_service.users(tg_id=tg_id)
    data = [
        (user.user_id, user.name, user.tg_id,
         user.adress, user.telephone, "admin" if user.admin else "not admin") for user in users_data
    ]
    return {
        "users": data
    }


async def get_user_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    user = await user_service.get_user(user_id=int(item_id))
    await user_service.update_user(user_id=int(item_id),
                                   tg_id=user.tg_id,
                                   admin=(not user.admin))


users_window = Window(
    Const("Сделать пользователя админом (удалить из админов)"),
    ScrollingGroup(
        Select(
            text=Format(html.quote("{item[1]} | {item[2]} | {item[3]} | {item[4]} - {item[5]}")),
            item_id_getter=operator.itemgetter(0),
            items="users",
            id="user_i",
            on_click=get_user_button
        ),
        id="users_group",
        width=1,
        height=10,
    ),
    state=User.users,
    getter=users_getter
)

user_search_windows = [tg_id_filter_window, users_search_window, users_window]
