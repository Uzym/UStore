
import operator
from typing import List, Any, Dict

from aiogram import html, F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, Back, Group, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const, Case

from src.states.states import Main, Project, Section, Card
from src.windows.card.window.comment import comments_button
from src.windows.card.window.to_card_button import to_card_button
from src.windows.card.window.user import users_project_button
from src.windows.main.window.to_main_menu_button import to_main_menu_button
from src.lexicon import LEXICON
from src.models import domain
from src.services import CardService
from src.services.project_service import parse_link_project, ProjectService
from src.windows.project.window.to_project_button import to_project_button
from src.windows.section.window.to_section_button import to_section_button

card_service = CardService()
project_service = ProjectService()

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


def update_section_include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data.get("card_actions")
    for action in actions:
        if action[0] == "complete_card" or action[0] == "update_card":
            return True
    return False


card_update_section_button = Button(
    text=Const(LEXICON["card_update_section"]),
    id="card_update_section_button",
    on_click=lambda callback, button, manager: manager.switch_to(Card.update_section),
    when=update_section_include_button
)


async def sections_getter(dialog_manager: DialogManager, **kwargs):
    project_id = int(dialog_manager.start_data["project_id"])
    section_id = int(dialog_manager.start_data["section_id"])
    sections = await project_service.get_sections(project_id)
    sections_data = []
    for section in sections:
        if section.section_id == section_id:
            continue
        sections_data.append((section.title, section.section_id))
    return {
        "card_sections": sections_data
    }


async def update_card_section(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    try:
        card_id = int(manager.start_data["card_id"])
        section = await card_service.update_card(card_id, section_id=int(item_id))
        manager.start_data["section_id"] = str(section.section_id)
        await manager.switch_to(Card.card)
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


update_section_card_window = Window(
    Const(LEXICON["card_update_section"]),
    Select(
        Format("{item[0]}"),
        id="s_sections_card",
        item_id_getter=operator.itemgetter(1),
        items="card_sections",
        on_click=update_card_section
    ),
    to_card_button,
    getter=sections_getter,
    state=Card.update_section
)

card_action_buttons = [
    Group(
        users_project_button,
        card_update_button,
        comments_button,
        complete_card_button,
        card_update_section_button,
        width=2,
        when=F["start_data"]["update_card_visible"].is_not(True)
    ),
    Group(
        to_section_button,
        width=1,
        when=F["start_data"]["update_card_visible"].is_not(True)
    )
]
