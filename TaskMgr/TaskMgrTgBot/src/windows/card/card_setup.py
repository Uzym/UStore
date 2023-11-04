from datetime import datetime

from aiogram import Router
from aiogram_dialog import DialogManager, StartMode, Dialog

from src.windows.card.window.card import card_window
from src.windows.card.window.update import update_card_windows

dialog: Dialog = Dialog(card_window, *update_card_windows)


def setup() -> Router():
    router = Router(name=__name__)

    return router, dialog
