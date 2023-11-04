from aiogram import Router
from aiogram_dialog import Dialog

from src.handlers.section.window.section import section_window
from src.handlers.section.window.update import update_section_windows

dialog: Dialog = Dialog(section_window, *update_section_windows)


def setup() -> Router():
    router = Router(name=__name__)

    return router, dialog
