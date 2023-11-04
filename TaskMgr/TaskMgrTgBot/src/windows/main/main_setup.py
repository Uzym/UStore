from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog

from src.lexicon.lexicon import START_COMMAND, HELP_COMMAND
from src.services import UserService
from src.states.states import Main
from src.windows.main.window.get_me_window import get_me_window
from src.windows.main.window.help_window import help_window
from src.windows.main.window.main_window import main_window


async def start_message(message: Message, user_service: UserService, dialog_manager: DialogManager):
    await user_service.create_user(name=message.from_user.full_name, telegram_id=str(message.from_user.id))
    await dialog_manager.start(Main.main, mode=StartMode.RESET_STACK)


async def help_message(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(Main.help, mode=StartMode.RESET_STACK)


dialog: Dialog = Dialog(main_window, get_me_window, help_window)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        start_message, Command(START_COMMAND)
    )
    router.message.register(
        help_message, Command(HELP_COMMAND)
    )

    return router, dialog
