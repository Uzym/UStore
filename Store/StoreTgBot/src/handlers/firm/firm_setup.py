from aiogram import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog
from src.handlers.firm.window.firms_search_window import search_firm_windows
from src.handlers.firm.window.firms_create_window import create_firm_windows
from src.handlers.firm.window.firm_update_window import update_firm_windows
from src.handlers.firm.window.firm_window import firm_window, firm_wait_photo_window, firm_delete_photos_window
from src.filters import IsAdmin
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


dialog: Dialog = Dialog(*create_firm_windows, *search_firm_windows, firm_window, *update_firm_windows,
                        firm_wait_photo_window, firm_delete_photos_window)  # TODO


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        firms, and_f(Command(FIRMS_COMMAND), IsAdmin(admin=True))
    )

    router.message.register(
        firm_create, and_f(Command(NEW_FIRM_COMMAND), IsAdmin(admin=True))
    )

    return router, dialog
