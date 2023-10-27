from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.services import TaskMgrApiService

router: Router = Router()

@router.message(Command(commands=["start"]))
async def start_message(message: Message):
    pass

@router.message(Command(commands=["help"]))
async def help_message(message: Message, task_mgr_api: TaskMgrApiService):
    pass

@router.message()
async def process_any_message(message: Message, task_mgr_api: TaskMgrApiService):
    await message.reply(text=message.text)