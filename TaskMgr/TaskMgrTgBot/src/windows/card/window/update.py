
import operator
from datetime import date, datetime
from typing import List, Any, Dict

from aiogram import html, F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Select, Back, Group, Row, Cancel, Calendar
from aiogram_dialog.widgets.text import Format, Const

from src.states.states import Main, Project, Section, Card
from src.windows.card.window.to_card_button import to_card_button
from src.windows.main.window.to_main_menu_button import to_main_menu_button
from src.lexicon import LEXICON
from src.models import domain
from src.services import CardService
from src.services.project_service import parse_link_project
from src.windows.project.window.to_project_button import to_project_button
from src.windows.section.window.to_section_button import to_section_button

card_service = CardService()


card_update_title_button = Button(
    text=Const(LEXICON["card_update_title"]),
    id="card_update_title_button",
    on_click=lambda callback,button,manager: manager.switch_to(Card.update_title)
)


async def update_title(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    card_id = int(manager.start_data["card_id"])
    await card_service.update_card(card_id=card_id, title=message.text)
    await manager.switch_to(Card.card)

card_update_title_window = Window(
    Const(LEXICON["card_update_title"]),
    MessageInput(update_title),
    to_card_button,
    state=Card.update_title
)

card_update_description_button = Button(
    text=Const(LEXICON["card_update_description"]),
    id="card_update_description_button",
    on_click=lambda callback,button,manager: manager.switch_to(Card.update_description)
)


async def update_description(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    card_id = int(manager.start_data["card_id"])
    await card_service.update_card(card_id=card_id, description=message.text)
    await manager.switch_to(Card.card)

card_update_description_window = Window(
    Const(LEXICON["card_update_description"]),
    MessageInput(update_description),
    to_card_button,
    state=Card.update_description
)

card_update_tags_button = Button(
    text=Const(LEXICON["card_update_tags"]),
    id="card_update_tags_button",
    on_click=lambda callback,button,manager: manager.switch_to(Card.update_tags)
)


async def tags_getter(dialog_manager: DialogManager, **kwargs):
    card_id = int(dialog_manager.start_data["card_id"])
    telegram_id = dialog_manager.start_data["telegram_id"]
    tags = (await card_service.get_card(card_id=card_id, telegram_id=telegram_id)).card.tags
    tags_data = [(tag, 1) for tag in tags]
    return {
        "card_tags": tags_data
    }


async def delete_tags(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    card_id = int(manager.start_data["card_id"])
    telegram_id = manager.start_data["telegram_id"]
    tags = (await card_service.get_card(card_id=card_id, telegram_id=telegram_id)).card.tags
    tags.remove(item_id)
    await card_service.update_card(card_id=card_id, tags=tags)


async def update_tags(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    card_id = int(manager.start_data["card_id"])
    telegram_id = manager.start_data["telegram_id"]
    tags = (await card_service.get_card(card_id=card_id, telegram_id=telegram_id)).card.tags
    tags.append(message.text.replace(" ", "_"))
    await card_service.update_card(card_id=card_id, tags=tags)

card_update_tags_window = Window(
    Const(html.bold(LEXICON["card_update_tags"])),
    Const(LEXICON["card_update_tags_message"]),
    Select(
        Format("{item[0]}"),
        id="s_tags",
        item_id_getter=operator.itemgetter(0),
        items="card_tags",
        on_click=delete_tags
    ),
    MessageInput(update_tags),
    to_card_button,
    getter=tags_getter,
    state=Card.update_tags
)

card_update_due_button = Button(
    text=Const(LEXICON["card_update_due"]),
    id="card_update_due_button",
    on_click=lambda callback,button,manager: manager.switch_to(Card.update_due)
)


async def update_due(callback: CallbackQuery, widget, manager: DialogManager, selected_date: date):
    card_id = int(manager.start_data["card_id"])
    await card_service.update_card(card_id=card_id, due=str(selected_date.isoformat()))
    await manager.switch_to(Card.card)

card_update_due_window = Window(
    Const(LEXICON["card_update_due"]),
    Calendar(id='calendar', on_click=update_due),
    to_card_button,
    state=Card.update_due
)

card_update_buttons = [
    Group(
        card_update_title_button,
        card_update_description_button,
        card_update_tags_button,
        card_update_due_button,
        width=2,
        when=F["start_data"]["update_card_visible"].is_not(False)
    ),
    Group(
        to_card_button,
        width=1,
        when=F["start_data"]["update_card_visible"].is_not(False)
    )
]

update_card_windows = [
    card_update_title_window, card_update_description_window,
    card_update_tags_window, card_update_due_window
]
