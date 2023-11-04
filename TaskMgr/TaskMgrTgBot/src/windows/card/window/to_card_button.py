from typing import Dict

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.states.states import Section, Card


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    try:
        manager.start_data["update_card_visible"] = False
        await manager.start(
            Card.card,
            data=manager.start_data
        )
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


to_card_button = Button(
    text=Const(LEXICON["back"]),
    id="to_card_menu",
    on_click=on_click_button,
)
