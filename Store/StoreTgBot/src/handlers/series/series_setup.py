from aiogram import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog
from src.filters import IsAdmin
from src.lexicon.lexicon import SERIES_COMMAND, NEW_SERIES_COMMAND, LEXICON
from src.states.states import Series

from src.handlers.series.window.series_search_window import search_series_windows
from src.handlers.series.window.series_create_window import create_series_windows
from src.handlers.series.window.series_update_window import update_series_windows
from src.handlers.series.window.series_window import (series_window, series_wait_photo_window,
                                                      series_delete_photos_window)


async def series(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Series.series_search,
                        mode=StartMode.RESET_STACK,
                        data={"telegram_id": str(message.from_user.id)})


async def series_create(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Series.series_create,
                        mode=StartMode.RESET_STACK,
                        data={"telegram_id": str(message.from_user.id)})

dialog: Dialog = Dialog(*create_series_windows, *search_series_windows, series_window,
                        *update_series_windows, series_wait_photo_window, series_delete_photos_window)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        series, and_f(Command(SERIES_COMMAND), IsAdmin(admin=True))
    )

    router.message.register(
        series_create, and_f(Command(NEW_SERIES_COMMAND), IsAdmin(admin=True))
    )

    return router, dialog
