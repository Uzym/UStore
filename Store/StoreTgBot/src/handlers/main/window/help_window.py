import operator
import logging
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, List, Format

from src.lexicon import LEXICON, COMMANDS
from src.states.states import Main
from src.handlers.main.window.to_main_menu_button import to_main_menu_button
from src.services import UserService

user_service = UserService()
logger = logging.getLogger()


async def help_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    try:
        await manager.switch_to(state=Main.help)
    except:
        await callback.answer(text=LEXICON["not_found"])


async def help_getter(dialog_manager: DialogManager, **kwargs):
    user = await user_service.users(tg_id=str(dialog_manager.event.from_user.id))
    if user[0].admin:
        data = [
                (com.command, com.description) for com in COMMANDS
        ]
    else:
        COMMON_COMMANDS = COMMANDS[0:4]
        data = [
            (com.command, com.description) for com in COMMON_COMMANDS
        ]
    return {
        "help_commands": data
    }


help_window = Window(
    Const(
        LEXICON["help"]
    ),
    List(
        Format("/{item[0]} - {item[1]}"),
        items="help_commands",
    ),
    to_main_menu_button,
    state=Main.help,
    getter=help_getter
)

help_button = Button(
    Const(LEXICON["help_button"]),
    id="help",
    on_click=help_button
)