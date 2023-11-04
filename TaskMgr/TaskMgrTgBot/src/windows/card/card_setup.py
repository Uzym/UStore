from datetime import datetime

from aiogram import Router
from aiogram_dialog import DialogManager, StartMode, Dialog

from src.windows.card.window.action import update_section_card_window
from src.windows.card.window.card import card_window
from src.windows.card.window.update import update_card_windows
from src.windows.card.window.user import users_card_windows
from src.windows.card.window.comment import comment_card_windows

dialog: Dialog = Dialog(card_window, *update_card_windows,
                        update_section_card_window, *users_card_windows,
                        *comment_card_windows)


def setup() -> Router():
    router = Router(name=__name__)

    return router, dialog
