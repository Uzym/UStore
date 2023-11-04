from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.states.states import Main


async def main_menu_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    try:
        await manager.switch_to(state=Main.main)
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


to_main_menu_button = Button(
    text=Const(LEXICON["main_menu_button"]),
    id="to_main_menu",
    on_click=main_menu_button,
)
