from aiogram import Router
from aiogram_dialog import Dialog

from src.handlers.card.window.action import update_section_card_window
from src.handlers.card.window.card import card_window
from src.handlers.card.window.comment import comment_card_windows
from src.handlers.card.window.update import update_card_windows
from src.handlers.card.window.user import users_card_windows

dialog: Dialog = Dialog(card_window, *update_card_windows,
                        update_section_card_window, *users_card_windows,
                        *comment_card_windows)


def setup() -> Router():
    router = Router(name=__name__)

    return router, dialog
