from datetime import datetime

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog

from src.lexicon.lexicon import PROJECTS_COMMAND, LEXICON, NEW_PROJECT_COMMAND
from src.services import UserService, ProjectService, RoleService
from src.states.states import Project
from src.windows.project.window.project_user import users_project_windows
from src.windows.project.window.project_window import project_window
from src.windows.project.window.projects_window import projects_window
from src.windows.project.window.project_update import update_project_windows

project_service = ProjectService()
user_service = UserService()
role_service = RoleService()


async def new_project(message: Message, dialog_manager: DialogManager):
    try:
        telegram_id = str(message.from_user.id)
        title = f"Проект {str(message.from_user.full_name)} от {str(datetime.now())}"
        description = "Это стандартное описания для проекта, измените его"
        project = await project_service.create_project(title, description)

        user = await user_service.users(telegram_id=telegram_id)
        role = await role_service.roles(
            description="telegram creator project role"
        )

        await project_service.add_user_to_project(
            project_id=project.project_id,
            role_id=role[0].role_id,
            user_id=user[0].user_id
        )

        await message.answer(LEXICON["new_project_good"])

        try:
            await dialog_manager.done()
        except:
            pass
        await dialog_manager.start(Project.project_update,
                                   mode=StartMode.RESET_STACK,
                                   data={
                                       "telegram_id": str(message.from_user.id),
                                       "project_id": str(project.project_id)
                                   })
    except:
        await message.answer(LEXICON["not_found"])


async def projects(message: Message, dialog_manager: DialogManager):
    try:
        try:
            await dialog_manager.done()
        except:
            pass
        await dialog_manager.start(Project.projects,
                                   mode=StartMode.RESET_STACK,
                                   data={"telegram_id": str(message.from_user.id)})
    except:
        await message.answer(text=LEXICON["not_found"])


dialog: Dialog = Dialog(projects_window, project_window, *update_project_windows, *users_project_windows)


def setup() -> Router():
    router = Router(name=__name__)
    router.message.register(
        projects, Command(PROJECTS_COMMAND)
    )
    router.message.register(
        new_project, Command(NEW_PROJECT_COMMAND)
    )

    return router, dialog
