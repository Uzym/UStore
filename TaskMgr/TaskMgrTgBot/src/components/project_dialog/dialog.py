import operator
from typing import Any

from aiogram import html
from aiogram.types import BotCommand, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Data
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const
from emoji import emojize

from generated import taskmgr
from .state import ProjectDialog
from src.utils.dialog_builder import DialogBuilder
from src.utils.window_builder import WindowBuilder
from .. import project_dialog
from ..input_dialog.dialog import to_variable, input_variable, start_variable
from ..input_dialog.state import InputDialog
from ..section_dialog.state import SectionDialog
from ..select_object_dialog.state import SelectObjectDialog
from ...lexicon.lexicon import title_lexicon, project_lexicon, description_lexicon, view_lexicon, section_lexicon, \
    card_lexicon
from ...services import ProjectService
from ...services.odata_service import MyODataService
from ...utils.variable_generator import VariableGenerator


async def on_click_select_section(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=SelectObjectDialog.section_list,
        data={
            to_variable: button_local.widget_id,
            start_variable: True,
            str(VariableGenerator(str(taskmgr.Project.ProjectId))):
                manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))]
        }
    )

section_select_button = Button(
    id=str(VariableGenerator(str(taskmgr.Sections.SectionId))),
    text=Const(str(section_lexicon.many)),
    on_click=on_click_select_section
)


async def item_getter(dialog_manager: DialogManager, **kwargs):
    print(dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))])
    odata_service: MyODataService = MyODataService.instance
    q1 = odata_service.service.query(taskmgr.Projects)
    q1 = q1.filter(
        taskmgr.Projects.ProjectId == dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))]
    )
    project = q1.first()

    return {
        str(VariableGenerator(str(taskmgr.Project.Title))): project.Title,
        str(VariableGenerator(str(taskmgr.Project.Description))): project.Description
    }


async def on_click_select_card(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=SelectObjectDialog.card_list,
        data={
            to_variable: button_local.widget_id,
            start_variable: True,
            str(VariableGenerator(str(taskmgr.Project.ProjectId))): manager.start_data[
                str(VariableGenerator(str(taskmgr.Project.ProjectId)))
            ]
        }
    )

card_select_button = Button(
    id=str(VariableGenerator(str(taskmgr.Cards.CardId))),
    text=Const(str(card_lexicon.many)),
    on_click=on_click_select_card
)

item = WindowBuilder(
    title=str(view_lexicon),
    state=ProjectDialog.item
).add_widget(
    VariableGenerator(str(taskmgr.Project.Title)).format_title()
).add_widget(
    VariableGenerator(str(taskmgr.Project.Description)).format_description()
).add_widget(
    card_select_button
).set_getter(
    item_getter
).add_widget(
    section_select_button
)


async def on_click_update_string(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=InputDialog.string,
        data={
            to_variable: button_local.widget_id,
        }
    )

update_title_button = Button(
    id="update_title",
    text=Const(str(title_lexicon.update)),
    on_click=on_click_update_string
)

update_description_button = Button(
    id="update_description",
    text=Const(str(description_lexicon.update)),
    on_click=on_click_update_string
)

update = WindowBuilder(
    title=str(project_lexicon.update),
    state=ProjectDialog.update
).add_widget(
    VariableGenerator(str(taskmgr.Project.Title)).format_title()
).add_widget(
    VariableGenerator(str(taskmgr.Project.Title)).format_description()
).add_widget(
    update_title_button
).add_widget(
    update_description_button
).set_getter(
    item_getter
)


async def process_result(start_data: Data, result: Any, dialog_manager: DialogManager):
    if result is None:
        return
    project_service = ProjectService.instance
    if result[to_variable] == update_title_button.widget_id:
        await project_service.update_project(
            project_id=int(dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))]),
            title=result[input_variable]
        )
    elif result[to_variable] == update_description_button.widget_id:
        await project_service.update_project(
            project_id=dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))],
            description=result[input_variable]
        )
    elif result[to_variable] == section_select_button.widget_id:
        await dialog_manager.start(
            state=SectionDialog.item,
            data={
                str(VariableGenerator(str(taskmgr.Section.SectionId))): result[input_variable]
            }
        )

dialog_b = DialogBuilder(
    title=str(project_lexicon)
).add_window(
    window_builder=item
).add_window(
    window_builder=update
).set_on_process_result(
    process_result
).set_arbitrary_navigation(
).apply_configuration()

button = dialog_b.get_button()
dialog = dialog_b.get_dialog()
