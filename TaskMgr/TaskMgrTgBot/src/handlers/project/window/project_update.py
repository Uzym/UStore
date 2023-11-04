from typing import Dict

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Row, Cancel
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.services import ProjectService
from src.states.states import Project
from src.handlers.project.window.to_project_button import to_project_button

project_service = ProjectService()


async def update_title(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    project_id = manager.start_data["project_id"]
    await project_service.update_project(project_id=project_id, title=message.text)
    await manager.switch_to(Project.project_update)


async def on_click_update_title_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Project.project_update_title)

update_project_title_button = Button(
    text=Const(LEXICON["update_project_title"]),
    id="update_project_title",
    on_click=on_click_update_title_button
)

update_project_title_window = Window(
        Const(LEXICON["update_project_title"]),
        MessageInput(update_title),
        Row(to_project_button, Cancel(Const(LEXICON["cancel"]))),
        state=Project.project_update_title
)


async def update_description(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    project_id = manager.start_data["project_id"]
    await project_service.update_project(project_id=project_id, description=message.text)
    await manager.switch_to(Project.project_update)


async def update_project_description_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Project.project_update_description)

update_project_description_button = Button(
    text=Const(LEXICON["update_project_description"]),
    id="update_project_description",
    on_click=update_project_description_button
)

update_project_description_window = Window(
        Const(LEXICON["update_project_description"]),
        MessageInput(update_description),
        Row(to_project_button, Cancel(Const(LEXICON["cancel"]))),
        state=Project.project_update_description
)


def include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data.get("project_actions")
    for action in actions:
        if action[0] == "update_project":
            return True
    return False


async def on_click_update_project_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await manager.switch_to(Project.project_update)


update_project_button = Button(
    text=Const(LEXICON["update"]),
    on_click=on_click_update_project_button,
    id="update_project_button",
    when=include_button
)


update_project_window = Window(
    Const(LEXICON["update"]),
    Group(
        update_project_title_button,
        update_project_description_button,
        width=2
    ),
    to_project_button,
    state=Project.project_update,
)

update_project_windows = [update_project_window, update_project_title_window, update_project_description_window]
