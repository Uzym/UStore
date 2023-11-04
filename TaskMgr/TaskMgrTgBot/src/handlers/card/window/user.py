import operator
from typing import Dict

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Format, Const, List, Case

from src.lexicon import LEXICON
from src.services import ProjectService, UserService, RoleService, CardService
from src.states.states import Card
from src.handlers.card.window.to_card_button import to_card_button

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
    manager.dialog_data["user_add_stage"] = "await_user_select"
    await manager.switch_to(Card.add_user)

add_user_button = Button(
    text=Const(LEXICON["add"]),
    id="add_user_card_button",
    when=add_user_include_button,
    on_click=add_user_on_click_button
)


async def add_user_getter(dialog_manager: DialogManager, **kwargs):
    project_id = int(dialog_manager.start_data["project_id"])

    user_roles = await project_service.get_users(project_id)
    users = []
    for user_role in user_roles:
        user = await user_service.get_user(user_role.user_id)
        role = await role_service.get_role(user_role.role_id)
        users.append(
            (user.name, role.title, user.telegram_id, user.user_id)
        )

    roles_data = await role_service.roles(table="card")
    roles = [(role.title, role.role_id) for role in roles_data]
    return {
        "users": users,
        "roles": roles
    }


async def user_on_click(callback: CallbackQuery, button: Button, manager: DialogManager, item_id: str):
    manager.dialog_data["add_user_id"] = item_id
    manager.dialog_data["user_add_stage"] = "await_user_role_select"


async def role_on_click(callback: CallbackQuery, button: Button, manager: DialogManager, item_id: str):
    user_id = int(manager.dialog_data["add_user_id"])
    role_id = int(item_id)
    card_id = int(manager.start_data["card_id"])
    await card_service.add_user(role_id=role_id, card_id=card_id, user_id=user_id)
    await manager.switch_to(Card.users)

add_user_card_window = Window(
    Const(LEXICON["add"]),
    Case(
        {
            "await_user_select": List(Format('{pos} <a href="tg://user?id={item[2]}">{item[0]}</a>'), items="users"),
            "await_user_role_select": Const(LEXICON["await_user_role_select"])
        },
        selector=F["dialog_data"]["user_add_stage"]
    ),
    Select(
        Format("{pos}: {item[0]}"),
        id="s_user_card",
        items="users",
        item_id_getter=operator.itemgetter(3),
        on_click=user_on_click,
        when=F["dialog_data"]["user_add_stage"] == "await_user_select"
    ),
    Select(
        Format("{pos}: {item[0]}"),
        id="s_role_card",
        items="roles",
        item_id_getter=operator.itemgetter(1),
        on_click=role_on_click,
        when=F["dialog_data"]["user_add_stage"] == "await_user_role_select"
    ),
    to_card_button,
    getter=add_user_getter,
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
