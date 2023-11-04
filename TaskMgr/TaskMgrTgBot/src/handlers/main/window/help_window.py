from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, List, Format

from src.lexicon import LEXICON, COMMANDS
from src.states.states import Main
from src.handlers.main.window.to_main_menu_button import to_main_menu_button


async def help_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    try:
        await manager.switch_to(state=Main.help)
    except:
        await callback.answer(text=LEXICON["not_found"])

help_window = Window(
    Const(
        LEXICON["help"]
    ),
    List(
        Format("- /{item[0]} - {item[1]}"),
        items=COMMANDS
    ),
    to_main_menu_button,
    state=Main.help,
)

help_button = Button(
    Const(LEXICON["help_button"]),
    id="help",
    on_click=help_button
)
