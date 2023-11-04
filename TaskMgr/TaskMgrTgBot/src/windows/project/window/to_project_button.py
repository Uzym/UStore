from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.states.states import Project


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    try:
        await manager.start(
            Project.project,
            data=manager.start_data
        )
        # await manager.switch_to(state=Project.project)
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


to_project_button = Button(
    text=Const(LEXICON["back"]),
    id="to_project_menu",
    on_click=on_click_button,
)
