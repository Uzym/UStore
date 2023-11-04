import operator

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group
from aiogram_dialog.widgets.text import Format

from src.lexicon import LEXICON
from src.services import ProjectService
from src.states.states import Project
from src.handlers.project.window.project_window import get_project_button

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
