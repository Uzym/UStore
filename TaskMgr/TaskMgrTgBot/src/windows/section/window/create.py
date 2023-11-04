from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.services import ProjectService
from src.states.states import Section

project_service = ProjectService()


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    try:
        project_id = manager.start_data["project_id"]
        title = f"Список {str(callback.from_user.full_name)} от {str(datetime.now())}"
        section = await project_service.add_section_to_project(project_id=project_id, title=title)
        manager.start_data["section_id"] = str(section.section_id)
        await manager.start(
            Section.update,
            data=manager.start_data
        )
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


create_section_button = Button(
    text=Const(LEXICON["add"]),
    id="create_section_button",
    on_click=on_click_button,
)
