from aiogram import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog
from src.filters import IsAdmin
from src.lexicon.lexicon import PRODUCTS_COMMAND, NEW_PRODUCT_COMMAND, LEXICON
from src.states.states import Product

from src.handlers.product.window.product_search_window import search_product_windows
from src.handlers.product.window.product_create_window import create_product_windows
from src.handlers.product.window.product_update_window import update_product_windows
from src.handlers.product.window.product_window import (product_window, product_wait_photo_window,
                                                        product_delete_photos_window)


async def products(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Product.products_search,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})


async def product_create(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Product.product_create,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})

dialog: Dialog = Dialog(*create_product_windows, *search_product_windows, product_window,
                        *update_product_windows,
                        product_wait_photo_window, product_delete_photos_window)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        products, and_f(Command(PRODUCTS_COMMAND), IsAdmin(admin=True))
    )

    router.message.register(
        product_create, and_f(Command(NEW_PRODUCT_COMMAND), IsAdmin(admin=True))
    )

    return router, dialog
