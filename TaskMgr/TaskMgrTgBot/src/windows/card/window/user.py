import operator
from typing import Any, Dict

from aiogram import html
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Button, ScrollingGroup, Back, Select, Url
from aiogram_dialog.widgets.text import Format, Const, List

from src.states.states import Main, Project, Card
from src.windows.card.window.to_card_button import to_card_button
from src.windows.main.window.to_main_menu_button import to_main_menu_button
from src.lexicon import LEXICON
from src.models import domain
from src.services import ProjectService, UserService, RoleService, CardService
from src.services.project_service import parse_link_project
from src.windows.project.window.to_project_button import to_project_button
from src.windows.project.window.project_add_user import add_user_project_button, add_user_project_window

project_service = ProjectService()
card_service = CardService()
user_service = UserService()
role_service = RoleService()


def add_user_include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data["card_actions"]
    for action in actions:
        if action[0] == "add_user_card":
            return True
    return False


async def add_user_on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await manager.switch_to(Card.add_user)

add_user_button = Button(
    text=Const(LEXICON["add"]),
    id="add_user_card_button",
    when=add_user_include_button,
    on_click=add_user_on_click_button
)

add_user_card_window = Window(
    Const(LEXICON["add"]),
    to_card_button,
    state=Card.add_user
)


def include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data["card_actions"]
    for action in actions:
        if action[0] == "get_user_card":
            return True
    return False


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await manager.switch_to(Card.users)


async def getter(dialog_manager: DialogManager, **kwargs):
    card_id = int(dialog_manager.start_data["card_id"])

    user_roles = await card_service.get_users(card_id)
    users = []
    for user_role in user_roles:
        user = await user_service.get_user(user_role.user_id)
        role = await role_service.get_role(user_role.role_id)
        users.append(
            (user.name, role.title, user.telegram_id)
        )
    return {
        "users": users
    }


users_project_button = Button(
    text=Const(LEXICON["users"]),
    on_click=on_click_button,
    id="users_project",
    when=include_button
)

users_card_window = Window(
    Const(LEXICON["users"]),
    List(
        Format('<a href="tg://user?id={item[2]}">{item[0]}</a> - {item[1]}'),
        items="users"
    ),
    add_user_button,
    to_card_button,
    getter=getter,
    state=Card.users,
)

users_card_windows = [users_card_window, add_user_card_window]
