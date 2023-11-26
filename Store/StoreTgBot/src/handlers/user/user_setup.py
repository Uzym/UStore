from aiogram import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog
from src.filters import IsAdmin
from src.lexicon.lexicon import USERS_COMMAND, LEXICON
from src.states.states import User

from src.handlers.user.window.user_search_window import user_search_windows


async def users(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        pass
    await dialog_manager.start(User.users_search,
                               mode=StartMode.RESET_STACK,
                               data={"telegram_id": str(message.from_user.id)})


dialog: Dialog = Dialog(*user_search_windows)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        users, and_f(Command(USERS_COMMAND), IsAdmin(admin=True))
    )

    return router, dialog
