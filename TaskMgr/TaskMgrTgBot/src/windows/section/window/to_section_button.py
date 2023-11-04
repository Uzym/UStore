from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.states.states import Section


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    try:
        await manager.start(
            Section.section,
            data=manager.start_data
        )
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


to_section_button = Button(
    text=Const(LEXICON["back"]),
    id="to_section_menu",
    on_click=on_click_button,
)
