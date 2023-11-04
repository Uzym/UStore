import operator
from typing import List, Any

from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Select, Group
from aiogram_dialog.widgets.text import Format, Const

from src.states.states import Main, Project
from src.windows.main.window.to_main_menu_button import to_main_menu_button
from src.lexicon import LEXICON
from src.models import domain
from src.services import ProjectService
from src.windows.project.window.project_window import get_project_button

project_service = ProjectService()


async def projects_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.start_data["telegram_id"]
    projects_data = await project_service.projects(telegram_id=telegram_id)
    data = [
        (project.title, str(project.project_id)) for project in projects_data
    ]
    return {
        "projects": data
    }


projects_window = Window(
    Format(LEXICON["projects"]),
    Group(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            id="projects_select",
            items="projects",
            on_click=get_project_button
        ),
        width=1
    ),
    getter=projects_getter,
    state=Project.projects,
)
