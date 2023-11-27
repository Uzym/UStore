from aiogram import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog
from src.filters import IsAdmin
from src.lexicon.lexicon import CATEGORIES_COMMAND, NEW_CATEGORY_COMMAND, LEXICON
from src.states.states import Category

from src.handlers.category.window.categories_search_window import search_category_windows
from src.handlers.category.window.categories_create_window import create_category_windows
from src.handlers.category.window.category_update_window import update_category_windows
from src.handlers.category.window.category_window import (category_window, category_wait_photo_window,
                                                          category_delete_photos_window)


async def categories(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Category.categories_search,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})


async def category_create(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Category.category_create,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})

dialog: Dialog = Dialog(*create_category_windows, *search_category_windows, category_window,
                        *update_category_windows, category_wait_photo_window, category_delete_photos_window)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        categories, and_f(Command(CATEGORIES_COMMAND), IsAdmin(admin=True))
    )

    router.message.register(
        category_create, and_f(Command(NEW_CATEGORY_COMMAND), IsAdmin(admin=True))
    )

    return router, dialog
