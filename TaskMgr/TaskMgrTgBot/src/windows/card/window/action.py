
import operator
from typing import List, Any, Dict

from aiogram import html, F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, Back, Group, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const, Case

from src.states.states import Main, Project, Section
from src.windows.main.window.to_main_menu_button import to_main_menu_button
from src.lexicon import LEXICON
from src.models import domain
from src.services import CardService
from src.services.project_service import parse_link_project
from src.windows.project.window.to_project_button import to_project_button
from src.windows.section.window.to_section_button import to_section_button

card_service = CardService()


def update_include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data.get("card_actions")
    for action in actions:
        if action[0] == "update_card":
            return True
    return False


async def update_card_on_click(callback: CallbackQuery, button: Button, manager: DialogManager):
    manager.start_data["update_card_visible"] = True


card_update_button = Button(
    text=Const(LEXICON["update"]),
    id="card_update_button",
    when=update_include_button,
    on_click=update_card_on_click
)


def complete_include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data.get("card_actions")
    for action in actions:
        if action[0] == "complete_card" or action[0] == "uncomplete_card":
            return True
    return False


async def complete_on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    try:
        card_id = int(manager.start_data["card_id"])
        if manager.dialog_data["complete"]:
            await card_service.uncomplete_card(card_id)
        else:
            await card_service.complete_card(card_id)
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


complete_card_button = Button(
    text=Case(
        texts={
            True: Const(LEXICON["cancel"]),
            False: Const(LEXICON["ok"])
        },
        selector=F["dialog_data"]["complete"]
    ),
    id="complete_card_button",
    on_click=complete_on_click_button,
    when=complete_include_button
)


card_action_buttons = [
    Group(
        card_update_button,
        complete_card_button,
        width=2,
        when=F["start_data"]["update_card_visible"].is_not(True)
    ),
    Group(
        to_section_button,
        width=1,
        when=F["start_data"]["update_card_visible"].is_not(True)
    )
]
