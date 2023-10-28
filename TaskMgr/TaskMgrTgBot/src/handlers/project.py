from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from src.lexicon import LEXICON

from src.services import ProjectService

router: Router = Router()

@router.message(Command(commands=["new_project"]))
async def new_project(message: Message, project_service: ProjectService):
    response = (await project_service.create_project(title="title", description="desc"))
    await message.answer(str(response))

@router.message(Command(commands=["update_projects"]))
async def update_project(message: Message, project_service: ProjectService):
    response = (await project_service.update_project(2, title="Я АМЕРИКАНЕЦ"))
    await message.answer(str(response))


@router.message(Command(commands=["get_users"]))
async def add_user(message: Message, project_service: ProjectService):
    response = (await project_service.get_users(str(2)))
    await message.answer(str(response))
