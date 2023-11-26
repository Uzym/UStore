from typing import Any

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager

from generated import taskmgr
from src.components.input_dialog.dialog import start_variable, input_variable, to_variable
from src.components.project_dialog.state import ProjectDialog
from src.components.select_object_dialog.state import SelectObjectDialog
from src.lexicon.lexicon import project_lexicon, list_lexicon
from src.services.odata_service import MyODataService
from src.utils.variable_generator import VariableGenerator
from src.utils.window_builder import WindowBuilder


async def on_click_item_project(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    if manager.start_data[start_variable]:
        await manager.start(
            state=ProjectDialog.item,
            data={
                str(VariableGenerator(str(taskmgr.Project.ProjectId))): int(item_id)
            }
        )
    else:
        await manager.done(
            result={
                input_variable: int(item_id),
                to_variable: manager.start_data[to_variable]
            }
        )


async def project_getter(dialog_manager: DialogManager, **kwargs):
    odata_service: MyODataService = MyODataService.instance
    q1 = odata_service.service.query(taskmgr.UserProjects)
    q1 = q1.expand(taskmgr.UserProjects.User)
    q1 = q1.expand(taskmgr.UserProjects.Project)
    q1 = q1.filter(taskmgr.UserProjects.User.TelegramId == str(dialog_manager.event.from_user.id))
    q1 = q1.select(taskmgr.UserProjects.Project)
    projects = q1.all()

    return {
        str(VariableGenerator(str(taskmgr.Projects))): [
            (
                str(project_item["Project"]["ProjectId"]),
                str(project_item["Project"]["Title"])
            ) for project_item in projects
        ]
    }


project_list = WindowBuilder(
    title=str(project_lexicon.many),
    state=SelectObjectDialog.project_list
).add_simple_select(
    on_click_item_project, str(VariableGenerator(str(taskmgr.Projects))), 10, 2
).set_getter(
    project_getter
).set_navigation(
    [str(list_lexicon)]
)