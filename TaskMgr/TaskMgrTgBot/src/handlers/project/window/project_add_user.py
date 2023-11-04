import operator
from typing import Any, Dict

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select
from aiogram_dialog.widgets.text import Format, Const, Case, List
from magic_filter import F

from src.lexicon import LEXICON
from src.services import ProjectService, UserService, RoleService
from src.states.states import Project
from src.handlers.project.window.to_project_button import to_project_button

project_service = ProjectService()
user_service = UserService()
role_service = RoleService()


def include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data["project_actions"]
    for action in actions:
        if action[0] == "add_user_project":
            return True
    return False


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    manager.dialog_data["user_add_stage"] = "await_user_name"
    manager.dialog_data["search_user_name"] = ""
    await manager.switch_to(Project.project_add_user)


add_user_project_button = Button(
    text=Const(LEXICON["add"]),
    on_click=on_click_button,
    id="add_user_project",
    when=include_button
)


async def user_request(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    try:
        manager.dialog_data["search_user_name"] = message.text
        manager.dialog_data["user_add_stage"] = "await_user_select"

    except:
        await message.answer(LEXICON["not_found"])
    pass


async def role_getter(dialog_manager: DialogManager, **kwargs):
    roles = await role_service.roles(table="project")
    users = []
    if dialog_manager.dialog_data.get("search_user_name") != "":
        users = await user_service.users(name=dialog_manager.dialog_data["search_user_name"])
    return {
        "roles": [(role.title, role.role_id) for role in roles],
        "users": [(user.name, str(user.user_id), user.telegram_id) for user in users]
    }


async def on_click_user(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.dialog_data["user_add_stage"] = "await_user_role_select"
    manager.dialog_data["user_id"] = item_id
    await callback.answer(LEXICON["loading"])


async def on_click_role(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    manager.dialog_data["user_add_stage"] = "user_added"
    await callback.answer(LEXICON["loading"])
    project_id = int(manager.start_data["project_id"])
    user_id = int(manager.dialog_data["user_id"])
    user_role = await project_service.add_user_to_project(role_id=int(item_id), project_id=project_id, user_id=user_id)

add_user_project_window = Window(
    Const(LEXICON["add_user_project"]),
    Case(
        {
            "await_user_name": Const(LEXICON["start_add_user"]),
            "await_user_select": List(Format('{pos} <a href="tg://user?id={item[2]}">{item[0]}</a>'), items="users"),
            "await_user_role_select": Const("popa"),
            "user_added": Const(LEXICON["end_add_user"])
        },
        selector=F["dialog_data"]["user_add_stage"]
    ),
    MessageInput(user_request),
    Select(
        Format("{pos}: {item[0]}"),
        id="s_user",
        items="users",
        item_id_getter=operator.itemgetter(1),
        on_click=on_click_user,
        when=F["dialog_data"]["user_add_stage"] == "await_user_select"
    ),
    Select(
        Format("{pos}: {item[0]}"),
        id="s_role",
        items="roles",
        item_id_getter=operator.itemgetter(1),
        on_click=on_click_role,
        when=F["dialog_data"]["user_add_stage"] == "await_user_role_select"
    ),
    to_project_button,
    state=Project.project_add_user,
    getter=role_getter
)

