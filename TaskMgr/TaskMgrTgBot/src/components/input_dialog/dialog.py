from datetime import date
from typing import Any

from aiogram.enums import ContentType
from aiogram.types import Message, CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Calendar
from emoji import emojize

from src.components.input_dialog.state import InputDialog
from src.utils.dialog_builder import DialogBuilder
from src.utils.window_builder import WindowBuilder


input_variable = "input"
to_variable = "to"
start_variable = "start"


def result_gen(manager: DialogManager, data: Any) -> dict[str, Any]:
    return {
        input_variable: data,
        to_variable: manager.start_data[to_variable]
    }


async def get_string(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    await manager.done(
        result=result_gen(manager, message.text)
    )

string = WindowBuilder(
    title=emojize("Текст"),
    state=InputDialog.string
).add_widget(
    MessageInput(content_types=ContentType.TEXT, func=get_string)
)


async def get_date(callback: CallbackQuery, widget: Any, manager: DialogManager, selected_date: date):
    await manager.done(
        result=result_gen(manager, selected_date)
    )

date = WindowBuilder(
    title=emojize("Дата"),
    state=InputDialog.date
).add_widget(
    Calendar(
        id="input_data_w",
        on_click=get_date
    )
)


select_item = WindowBuilder(
    title=emojize("Выбор из списка"),
    state=InputDialog.select_item
)

dialog_b = DialogBuilder(
    title=emojize(":pencil:Ввод")
).add_window(
    window_builder=string
).add_window(
    window_builder=date
).add_window(
    window_builder=select_item
).apply_configuration()

string_button = dialog_b.get_button(InputDialog.string)
date_button = dialog_b.get_button(InputDialog.date)
select_item_button = dialog_b.get_button(InputDialog.select_item)
dialog = dialog_b.get_dialog()
