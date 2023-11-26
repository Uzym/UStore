from typing import Any, Dict

from aiogram.types import BotCommand, CallbackQuery
from aiogram_dialog import Dialog, Data, DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from emoji import emojize

from generated import taskmgr
from src.components.input_dialog.dialog import to_variable, input_variable, start_variable
from src.components.main_dialog.state import MainDialog
from src.components.project_dialog.state import ProjectDialog
from src.components.select_object_dialog.state import SelectObjectDialog
from src.lexicon.lexicon import menu_lexicon, main_lexicon, project_lexicon
from src.utils.dialog_builder import DialogBuilder
from src.utils.variable_generator import VariableGenerator
from src.utils.window_builder import WindowBuilder

from src.components.help_dialog import help_button


async def on_click_select_project(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=SelectObjectDialog.project_list,
        data={
            to_variable: button_local.widget_id,
            start_variable: True
        }
    )

project_select_button = Button(
    id=str(VariableGenerator(str(taskmgr.Projects.ProjectId))),
    text=Const(str(project_lexicon.many)),
    on_click=on_click_select_project
)

menu = WindowBuilder(
    title=str(menu_lexicon),
    state=MainDialog.menu
).set_command(
    command=BotCommand(command="start", description="перейти в главное меню")
).add_widget(
    help_button
).add_widget(
    project_select_button
)


async def process_result(start_data: Data, result: Any, dialog_manager: DialogManager):
    if result is None:
        return
    if result[to_variable] == project_select_button.widget_id:
        await dialog_manager.start(
            state=ProjectDialog.item,
            data={
                str(VariableGenerator(str(taskmgr.Project.ProjectId))): result[input_variable]
            }
        )

dialog_b = DialogBuilder(
    title=str(main_lexicon)
).add_window(
    window_builder=menu
).set_on_process_result(
    process_result
).set_arbitrary_navigation(
).apply_configuration()

button = dialog_b.get_button()
dialog = dialog_b.get_dialog()
