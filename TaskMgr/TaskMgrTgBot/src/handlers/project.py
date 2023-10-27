from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.services import TaskMgrApiService
from src.lexicon import LEXICON

router: Router = Router()

@router.message(Command(commands=["new_project"]))
async def new_project(message: Message, task_mgr_api: TaskMgrApiService):
    await message.answer(text=LEXICON["start"])

@router.message(Command(commands=["projects"]))
async def new_project(message: Message, task_mgr_api: TaskMgrApiService):
    await message.answer(text=LEXICON["start"])
