from typing import Dict

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Group, Row, Cancel
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.services import SectionService
from src.states.states import Section
from src.handlers.section.window.to_section_button import to_section_button

section_service = SectionService()


async def update_title(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    section_id = int(manager.start_data["section_id"])
    await section_service.update_section(section_id=section_id, title=message.text)
    await manager.switch_to(Section.update)


async def on_click_update_title_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Section.update_title)

update_section_title_button = Button(
    text=Const(LEXICON["update_section_title"]),
    id="update_section_title_button",
    on_click=on_click_update_title_button
)

update_section_title_window = Window(
        Const(LEXICON["update_section_title"]),
        MessageInput(update_title),
        Row(to_section_button, Cancel(Const(LEXICON["cancel"]))),
        state=Section.update_title
)


def include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data.get("section_actions")
    for action in actions:
        if action[0] == "update_section":
            return True
    return False


async def on_click_update_section_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await manager.switch_to(Section.update)


update_section_button = Button(
    text=Const(LEXICON["update"]),
    on_click=on_click_update_section_button,
    id="update_section_button",
    when=include_button
)


update_section_window = Window(
    Const(LEXICON["update"]),
    Group(
        update_section_title_button,
        width=2
    ),
    to_section_button,
    state=Section.update,
)

update_section_windows = [update_section_window, update_section_title_window]