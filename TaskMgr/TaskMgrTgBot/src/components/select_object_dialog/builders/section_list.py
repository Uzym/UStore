from typing import Any, Type

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from odata.query import Query

from generated import taskmgr
from generated.taskmgr import Sections
from src.components.input_dialog.dialog import start_variable, input_variable, to_variable
from src.components.section_dialog.state import SectionDialog
from src.components.select_object_dialog.state import SelectObjectDialog
from src.lexicon.lexicon import section_lexicon, list_lexicon, card_lexicon
from src.services import SectionService, ProjectService
from src.services.odata_service import MyODataService
from src.utils.variable_generator import VariableGenerator
from src.utils.window_builder import WindowBuilder


async def on_click_item_section(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    if manager.start_data[start_variable]:
        await manager.start(
            state=SectionDialog.item,
            data={
                str(VariableGenerator(str(taskmgr.Section.SectionId))): int(item_id)
            }
        )
    else:
        await manager.done(
            result={
                input_variable: int(item_id),
                to_variable: manager.start_data[to_variable]
            }
        )


async def sections_getter(dialog_manager: DialogManager, **kwargs):
    q: Query[Type[Sections]] = MyODataService.instance.service.query(Sections)
    if str(VariableGenerator(str(taskmgr.Project.ProjectId))) in dialog_manager.start_data.keys():
        q = q.filter(
            taskmgr.Sections.ProjectId == dialog_manager.start_data[
                str(VariableGenerator(str(taskmgr.Project.ProjectId)))
            ]
        )
    items = q.all()
    return {
        str(VariableGenerator(str(taskmgr.Sections))): [
            (
                str(item.SectionId),
                str(item.Title)
            ) for item in items
        ]
    }


async def on_click_section_create(callback: CallbackQuery, widget: Any, manager: DialogManager):
    project_service: ProjectService = ProjectService.instance
    item = await project_service.add_section_to_project(
        project_id=manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))],
        title="Без названия"
    )
    await manager.start(
        state=SectionDialog.update,
        data={
            str(VariableGenerator(str(taskmgr.Section.SectionId))): item.section_id
        }
    )

create_section_button = Button(
    id="create_card_button",
    text=Const(str(section_lexicon.create)),
    on_click=on_click_section_create
)

section_list = WindowBuilder(
    title=str(section_lexicon.many),
    state=SelectObjectDialog.section_list
).add_simple_select(
    on_click_item_section, str(VariableGenerator(str(taskmgr.Sections))), 10, 2
).add_widget(
    create_section_button
).set_getter(
    sections_getter
).set_navigation(
    [str(list_lexicon)]
)