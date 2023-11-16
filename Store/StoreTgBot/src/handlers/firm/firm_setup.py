from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog
from src.handlers.firm.window.firms_search_window import search_firm_windows
from src.handlers.firm.window.firms_create_window import create_firm_windows

from src.lexicon.lexicon import FIRMS_COMMAND, NEW_FIRM_COMMAND, LEXICON
from src.states.states import Firm


async def firms(message: Message, dialog_manager: DialogManager):
    # try:
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Firm.firms_search,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})


# except:
#     await message.answer(text=LEXICON["not_found"])


async def firm_create(message: Message, dialog_manager: DialogManager):
    # try:
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(Firm.firm_create,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})


# except:
#     await message.answer(text=LEXICON["not_found"])


dialog: Dialog = Dialog(*search_firm_windows, *create_firm_windows)  # TODO


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        firms, Command(FIRMS_COMMAND)
    )

    router.message.register(
        firm_create, Command(NEW_FIRM_COMMAND)
    )

    return router, dialog
