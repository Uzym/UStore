from aiogram import Router
from aiogram.filters import Filter
from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from src.components.input_dialog.dialog import start_variable
from src.utils.window_builder import WindowBuilder


class ToWindowCommand(Filter):
    async def __call__(self, message: Message):
        for builder in WindowBuilder.instances:
            if builder.command is None:
                continue
            if builder.command.command == message.text.replace("/", ""):
                return True
        return False


router = Router()


@router.message(ToWindowCommand())
async def command_handler(message: Message, dialog_manager: DialogManager):
    try:
        await dialog_manager.done()
    except:
        await message.answer("Запуск...")
    finally:
        state: State = None
        for builder in WindowBuilder.instances:
            if builder.command is None:
                continue
            if builder.command.command == message.text.replace("/", ""):
                state = builder.state

        await dialog_manager.start(state=state, mode=StartMode.RESET_STACK, data={
            start_variable: True
        })
