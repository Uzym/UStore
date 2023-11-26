from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog

from src.lexicon.lexicon import ORDERS_HISTORY_COMMAND, ORDER_COMMAND
from src.services import UserService
from src.states.states import Order

from src.handlers.order.window.orders_history_window import orders_history_windows
from src.handlers.order.window.order_window import order_windows


async def orders_history(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Order.orders_history,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})


async def current_order(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Order.order,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})


dialog: Dialog = Dialog(*orders_history_windows, *order_windows)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        orders_history, Command(ORDERS_HISTORY_COMMAND)
    )
    router.message.register(
        current_order, Command(ORDER_COMMAND)
    )

    return router, dialog
