from datetime import datetime, date, timedelta
from typing import Any, Type

from aiogram.types import CallbackQuery, BotCommand
from aiogram_dialog import DialogManager, Data
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Format
from odata.query import Query

from generated import taskmgr
from generated.taskmgr import Sections, Cards
from src.components.input_dialog.dialog import start_variable, input_variable, to_variable
from src.components.input_dialog.state import InputDialog
from src.components.select_object_dialog.filter import CardFilter, get_filter_buttons
from src.components.select_object_dialog.state import SelectObjectDialog
from src.lexicon.lexicon import section_lexicon, list_lexicon, card_lexicon, calendar_lexicon, back_lexicon, \
    next_lexicon, cancel_lexicon, down_lexicon
from src.services.odata_service import MyODataService
from src.utils.variable_generator import VariableGenerator
from src.utils.window_builder import WindowBuilder


async def on_click_item_card(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    if manager.start_data[start_variable]:
        print(item_id)
        # await manager.start(
        #     state=SectionDialog.item,
        #     data={
        #         str(VariableGenerator(str(taskmgr.Section.SectionId))): int(item_id)
        #     }
        # )
    else:
        await manager.done(
            result={
                input_variable: int(item_id),
                to_variable: manager.start_data[to_variable]
            }
        )


async def cards_getter(dialog_manager: DialogManager, **kwargs):
    return await CardFilter(dialog_manager).list_view()


card_list = WindowBuilder(
    title=str(card_lexicon.many),
    state=SelectObjectDialog.card_list
).add_widget(
    get_filter_buttons()
).add_simple_select(
    on_click_item_card, str(VariableGenerator(str(Cards))), 10, 2
).set_getter(
    cards_getter
).set_navigation(
    [str(list_lexicon)]
)
