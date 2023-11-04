from aiogram_dialog.widgets.kbd import Row

from src.states.states import Main
from src.lexicon import LEXICON

from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const

from src.windows.main.window.get_me_window import get_me_button
from src.windows.main.window.help_window import help_button

main_window = Window(
    Const(LEXICON["main_window"]),
    Row(get_me_button, help_button),
    state=Main.main
)
