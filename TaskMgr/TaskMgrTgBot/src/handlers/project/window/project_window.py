import operator
from typing import Any

from aiogram import html
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Back, Group
from aiogram_dialog.widgets.text import Format, Const

from src.lexicon import LEXICON
from src.services import ProjectService
from src.services.project_service import parse_link_project
from src.states.states import Project
from src.handlers.project.window.project_update import update_project_button
from src.handlers.project.window.project_user import users_project_button
from src.handlers.section.window.create import create_section_button
from src.handlers.section.window.section import get_section_button

project_service = ProjectService()


async def project_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.start_data["telegram_id"]
    project_id = int(dialog_manager.start_data["project_id"])
    project_data = await project_service.get_project(telegram_id=telegram_id, project_id=project_id)
    actions = [
        parse_link_project(link) for link in project_data.links
    ]
    data_action = [
        (action[1] + "_project", f"{action[0]}") for action in actions
    ]

    sections_data = await project_service.get_sections(project_id)
    sections = [
        (section.title, str(section.section_id)) for section in sections_data
    ]

    dialog_manager.dialog_data["project_actions"] = data_action

    return {
        "project_title": project_data.project.title,
        "project_description": project_data.project.description,
        "sections": sections
    }


async def get_project_button(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    manager.start_data["project_id"] = item_id
    await manager.switch_to(Project.project)


project_window = Window(
    Format(html.bold(html.quote("{project_title}"))),
    Format(html.quote("{project_description}")),
    Group(
        update_project_button,
        users_project_button,
        width=2
    ),
    Group(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            id="sections_s",
            items="sections",
            on_click=get_section_button
        ),
        width=1
    ),
    create_section_button,
    Back(Const(LEXICON["back"])),
    getter=project_getter,
    state=Project.project,
)
