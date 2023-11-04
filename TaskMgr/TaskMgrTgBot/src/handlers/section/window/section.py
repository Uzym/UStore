import operator
from typing import Any

from aiogram import html
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup
from aiogram_dialog.widgets.text import Format
from emoji import emojize

from src.lexicon import LEXICON
from src.services import SectionService
from src.services.section_service import parse_link_section
from src.states.states import Section
from src.handlers.card.window.card import get_card_button
from src.handlers.card.window.create import create_card_button
from src.handlers.project.window.to_project_button import to_project_button
from src.handlers.section.window.update import update_section_button

section_service = SectionService()


async def section_getter(dialog_manager: DialogManager, **kwargs):
    telegram_id = dialog_manager.start_data["telegram_id"]
    section_id = int(dialog_manager.start_data["section_id"])
    section_data = await section_service.get_section(section_id, telegram_id)
    actions = [
        parse_link_section(link) for link in section_data.links
    ]
    data_action = [
        (action[1] + "_section", f"{action[0]}") for action in actions
    ]

    cards = await section_service.cards(section_id, telegram_id)
    cards_data = []
    for card in cards:
        name = str(card.title)
        if card.complete is not None:
            name += emojize(f" :check_mark_button:{card.complete[0:10]}")
        if card.due is not None:
            name += emojize(f" :spiral_calendar:{card.due[0:10]}")
        cards_data.append((str(card.card_id), name))

    dialog_manager.dialog_data["section_actions"] = data_action

    return {
        "section_title": section_data.section.title,
        "cards": cards_data
    }


async def get_section_button(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    manager.start_data["section_id"] = item_id
    await manager.start(
        Section.section,
        data=manager.start_data
    )


section_window = Window(
    Format(html.bold(html.quote("{section_title}"))),
    Group(
        update_section_button,
        width=2
    ),
    ScrollingGroup(
        Select(
            text=Format("{item[1]}"),
            item_id_getter=operator.itemgetter(0),
            id="cards_s",
            items="cards",
            on_click=get_card_button
        ),
        width=1,
        height=10,
        id="scrolling_cards"
    ),
    create_card_button,
    to_project_button,
    getter=section_getter,
    state=Section.section,
)
