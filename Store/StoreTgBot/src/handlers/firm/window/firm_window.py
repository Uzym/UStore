import operator
import logging

from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram import html
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import FirmService
from src.states.states import Firm

firm_service = FirmService()
logger = logging.getLogger()


async def firm_getter(dialog_manager: DialogManager, **kwargs):
    firm_id = int(dialog_manager.start_data['firm_id'])
    firm_data = await firm_service.get_firm(firm_id=firm_id)
    return {
        "firm_title": firm_data.title,
        "firm_description": firm_data.description,
        "firm_discount": firm_data.discount
    }


async def get_firm_button(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    manager.start_data['firm_id'] = item_id
    await manager.switch_to(Firm.firm)


firm_window = Window(
    Format("Фирма"),
    Format(html.bold(html.quote("{firm_title}"))),
    Format(html.quote("{firm_description}")),
    Format(html.quote("{firm_discount}")),
    Back(Const(LEXICON["back"])),
    Cancel(Const("Завершить")),
    state=Firm.firm,
    getter=firm_getter
)
