from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog

from src.lexicon.lexicon import START_COMMAND, HELP_COMMAND
from src.services import UserService
from src.states.states import Main
from src.handlers.main.window.get_me_window import (get_me_window, user_update_telephone_window,
                                                    user_update_email_window, user_update_address_window)
from src.handlers.main.window.help_window import help_window
from src.handlers.main.window.main_window import main_window

user_service = UserService()


async def start_message(message: Message, dialog_manager: DialogManager):
    user = await user_service.users(tg_id=str(dialog_manager.event.from_user.id))
    if len(user) == 0:
        await user_service.create_user(tg_id=str(message.from_user.id), name=message.from_user.full_name, admin=False)
    await dialog_manager.start(Main.main, mode=StartMode.RESET_STACK)


async def help_message(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Main.help, mode=StartMode.RESET_STACK)


dialog: Dialog = Dialog(main_window, get_me_window, help_window, user_update_telephone_window,
                        user_update_email_window, user_update_address_window)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        start_message, Command(START_COMMAND)
    )
    router.message.register(
        help_message, Command(HELP_COMMAND)
    )

    return router, dialog
