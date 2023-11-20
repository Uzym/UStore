import operator
import logging

from typing import Any
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import SeriesService, FirmService
from src.states.states import Series

series_service = SeriesService()
firm_service = FirmService()
logger = logging.getLogger()


async def series_create_go_back_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Series.series_create)


series_create_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="series_create_go_back",
    on_click=series_create_go_back_button
)


async def series_create_firms_list_param_button(callback: CallbackQuery, button: Button,
                                                manager: DialogManager, **kwargs):
    await manager.switch_to(Series.series_create_firms_list)


series_create_filter_firms_list_param_button = Button(
    text=Const("Задать фирму"),
    id="series_create_firms_list_param",
    on_click=series_create_firms_list_param_button
)


async def series_create_firm_id_param_button(callback: CallbackQuery, widget: Any, manager: DialogManager,
                                             item_id: str):
    await callback.answer(text=LEXICON["loading"])
    manager.start_data['firm_id'] = int(item_id)
    manager.dialog_data['firm_id'] = int(item_id)
    await manager.switch_to(Series.series_create)


async def series_create_firms_getter(manager: DialogManager, **kwargs):
    firms_data = await firm_service.firms()
    data = [
        (firm.title, str(firm.firm_id)) for firm in firms_data
    ]
    return {
        "firms": data
    }


series_create_firms_window = Window(
    Const(LEXICON["firms_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="firms",
            id="firm_i",
            on_click=series_create_firm_id_param_button
        ),
        id="firms_group",
        width=1,
        height=10,
    ),
    series_create_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Series.series_create_firms_list,
    getter=series_create_firms_getter
)


async def series_create_title_param_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Series.series_create_title_param)


async def series_create_title_param(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['title'] = message.text
    await manager.switch_to(Series.series_create)


series_create_title_param_button = Button(
    text=Const(LEXICON["select_title"]),
    id="series_create_title_param",
    on_click=series_create_title_param_button
)


series_create_title_param_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(series_create_title_param),
    Row(series_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_create_title_param
)


async def series_create_description_param_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Series.series_create_description_param)


async def series_create_description_param(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['description'] = message.text
    await manager.switch_to(Series.series_create)


series_create_description_param_button = Button(
    text=Const(LEXICON["select_description"]),
    id="series_create_description_param",
    on_click=series_create_description_param_button
)


series_create_description_param_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(series_create_description_param),
    Row(series_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_create_description_param
)


async def series_create_discount_param_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Series.series_create_discount_param)


async def series_create_discount_param(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['discount'] = float(message.text)
    await manager.switch_to(Series.series_create)


series_create_discount_param_button = Button(
    text=Const(LEXICON["select_discount"]),
    id="series_create_discount_param",
    on_click=series_create_discount_param_button
)


series_create_discount_param_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(series_create_discount_param),
    Row(series_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_create_discount_param
)


async def series_create_getter(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    title = None
    if 'title' in manager.dialog_data.keys():
        title = manager.dialog_data['title']
    description = None
    if 'description' in manager.dialog_data.keys():
        description = manager.dialog_data['description']
    discount = None
    if 'discount' in manager.dialog_data.keys():
        discount = manager.dialog_data['discount']
    firm_id = None
    if 'firm_id' in manager.dialog_data.keys():
        firm_id = manager.dialog_data['firm_id']
    series_data = await series_service.create_series(title=title, description=description,
                                                     discount=discount, firm_id=firm_id)
    manager.start_data['series_id'] = series_data.series_id
    manager.dialog_data['series_id'] = series_data.series_id
    await manager.switch_to(Series.series)


series_create_button = Button(
    text=Const(LEXICON["ok"]),
    id="series_create",
    on_click=series_create_getter
)


series_create_window = Window(
    Const(LEXICON["create_series"]),
    Group(
        series_create_filter_firms_list_param_button,
        series_create_title_param_button,
        series_create_description_param_button,
        series_create_discount_param_button,
        series_create_button,
        series_create_go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Series.series_create
)

create_series_windows = [series_create_firms_window,
                         series_create_title_param_window, series_create_description_param_window,
                         series_create_window, series_create_discount_param_window]
