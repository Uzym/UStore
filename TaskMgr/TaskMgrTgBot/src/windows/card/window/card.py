import operator
from typing import List, Any, Dict

from aiogram_dialog.widgets.common import Whenable
from emoji import emojize

from aiogram import html, F
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Select, Back, Group, ScrollingGroup
from aiogram_dialog.widgets.text import Format, Const, Case

from src.services.card_service import parse_link_card
from src.services.section_service import parse_link_section
from src.states.states import Section, Card
from src.lexicon import LEXICON
from src.models import domain
from src.services import ProjectService, SectionService, CardService
from src.windows.card.window.action import card_action_buttons
from src.windows.card.window.update import card_update_buttons
from src.windows.project.window.to_project_button import to_project_button
from src.windows.section.window.to_section_button import to_section_button
from src.windows.section.window.update import update_section_button

card_service = CardService()


async def card_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.start_data["telegram_id"]
    card_id = int(dialog_manager.start_data["card_id"])
    card = await card_service.get_card(card_id=card_id, telegram_id=telegram_id)

    actions = [
        parse_link_card(link) for link in card.links
    ]
    data_action = [
        (action[1] + "_card", f"{action[0]}") for action in actions
    ]

    dialog_manager.dialog_data["card_actions"] = data_action
    dialog_manager.dialog_data["complete"] = True if card.card.complete is not None else False

    tags = ""
    if len(card.card.tags) > 0:
        tags = "#" + " #".join(card.card.tags)
    tags += "\n"

    dates = ""
    if card.card.created is not None:
        dates += emojize(f":plus:{card.card.created[0:16]}\n")
    if card.card.due is not None:
        dates += emojize(f":spiral_calendar:{card.card.due[0:16]}\n")
    if card.card.complete is not None:
        dates += emojize(f":check_mark_button:{card.card.complete[0:16]}\n")

    return {
        "card_title": card.card.title,
        "card_description": card.card.description,
        "card_dates": dates,
        "card_tags": tags
    }


async def get_card_button(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    manager.start_data["card_id"] = item_id
    manager.start_data["update_card_visible"] = False
    await manager.start(
        Card.card,
        data=manager.start_data
    )


card_window = Window(
    Format(html.bold(html.quote("{card_title}"))),
    Format(html.italic(html.quote("{card_description}"))),
    Format(html.quote("{card_tags}")),
    Format("{card_dates}"),
    *card_update_buttons,
    *card_action_buttons,
    getter=card_getter,
    state=Card.card,
)
