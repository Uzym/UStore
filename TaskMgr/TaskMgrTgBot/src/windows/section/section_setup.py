from datetime import datetime

from aiogram import Router
from aiogram_dialog import DialogManager, StartMode, Dialog

from src.windows.section.window.section import section_window
from src.windows.section.window.update import update_section_windows

dialog: Dialog = Dialog(section_window, *update_section_windows)


def setup() -> Router():
    router = Router(name=__name__)

    return router, dialog
