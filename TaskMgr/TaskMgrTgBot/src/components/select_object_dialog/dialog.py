from typing import Any

from aiogram_dialog import Data, DialogManager
from emoji import emojize

from generated import taskmgr
from src.components.input_dialog.dialog import to_variable, input_variable
from src.components.select_object_dialog.builders.card_calendar import update_current_date_button, card_calendar
from src.components.select_object_dialog.builders.card_list import card_list
from src.components.select_object_dialog.builders.project_list import project_list
from src.components.select_object_dialog.builders.section_list import section_list
from src.components.select_object_dialog.filter import select_project_button, select_section_button
from src.components.select_object_dialog.state import SelectObjectDialog
from src.utils.dialog_builder import DialogBuilder
from src.utils.variable_generator import VariableGenerator


async def process_result(start_data: Data, result: Any, dialog_manager: DialogManager):
    if result is None:
        return
    if result[to_variable] == update_current_date_button.widget_id:
        dialog_manager.start_data[str(VariableGenerator("current_date"))] = result[input_variable]
    if result[to_variable] == select_project_button.widget_id:
        dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))] = result[input_variable]
    if result[to_variable] == select_section_button.widget_id:
        dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Section.SectionId)))] = result[input_variable]


dialog_b = DialogBuilder(
    title=emojize(":card_index_dividers:Выбор")
).add_window(
    window_builder=project_list
).add_window(
    window_builder=section_list
).add_window(
    window_builder=card_list
).add_window(
    window_builder=card_calendar
).set_on_process_result(
    process_result
).apply_configuration()

project_button = dialog_b.get_button(SelectObjectDialog.project_list)
section_button = dialog_b.get_button(SelectObjectDialog.section_list)
dialog = dialog_b.get_dialog()
