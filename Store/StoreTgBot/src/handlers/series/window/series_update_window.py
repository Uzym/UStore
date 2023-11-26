import operator
import logging

from typing import Any
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import SeriesService, FirmService
from src.states.states import Series

series_service = SeriesService()
firm_service = FirmService()
logger = logging.getLogger()


async def series_update_go_back_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Series.series_update)


series_update_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="series_update_go_back",
    on_click=series_update_go_back_button
)


async def series_update_firms_list_param_button(callback: CallbackQuery, button: Button,
                                                manager: DialogManager, **kwargs):
    await manager.switch_to(Series.series_create_firms_list)


series_update_filter_firms_list_param_button = Button(
    text=Const("Задать фирму"),
    id="series_update_firms_list_param",
    on_click=series_update_firms_list_param_button
)


async def series_update_firm_id_param_button(callback: CallbackQuery, widget: Any, manager: DialogManager,
                                             item_id: str):
    await callback.answer(text=LEXICON["loading"])
    manager.start_data['firm_id'] = int(item_id)
    manager.dialog_data['firm_id'] = int(item_id)
    await manager.switch_to(Series.series_update)


async def series_update_firms_getter(manager: DialogManager, **kwargs):
    firms_data = await firm_service.firms()
    data = [
        (firm.title, str(firm.firm_id)) for firm in firms_data
    ]
    return {
        "firms": data
    }


series_update_firms_window = Window(
    Const(LEXICON["firms_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="firms",
            id="firm_i",
            on_click=series_update_firm_id_param_button
        ),
        id="firms_group",
        width=1,
        height=10,
    ),
    series_update_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Series.series_update_firms_list,
    getter=series_update_firms_getter
)


async def series_update_title_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Series.series_update_title)


async def series_update_title(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['title'] = message.text
    await manager.switch_to(Series.series_update)


series_update_title_button = Button(
    text=Const(LEXICON["update_title"]),
    id="series_update_title_param",
    on_click=series_update_title_button
)

series_update_title_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(series_update_title),
    Row(series_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_update_title
)


async def series_update_description_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Series.series_update_description)


async def series_update_description(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['description'] = message.text
    await manager.switch_to(Series.series_update)


series_update_description_button = Button(
    text=Const(LEXICON["update_description"]),
    id="series_update_description_param",
    on_click=series_update_description_button
)

series_update_description_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(series_update_description),
    Row(series_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_update_description
)


async def series_update_discount_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Series.series_update_discount)


async def series_update_discount(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['discount'] = float(message.text)
    await manager.switch_to(Series.series_update)


series_update_discount_button = Button(
    text=Const(LEXICON["update_discount"]),
    id="series_update_discount_param",
    on_click=series_update_discount_button
)

series_update_discount_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(series_update_discount),
    Row(series_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_update_discount
)


async def series_update_getter(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    series_id = dialog_manager.dialog_data['series_id']
    title = None
    if 'title' in dialog_manager.dialog_data.keys():
        title = dialog_manager.dialog_data['title']
    description = None
    if 'description' in dialog_manager.dialog_data.keys():
        description = dialog_manager.dialog_data['description']
    discount = None
    if 'discount' in dialog_manager.dialog_data.keys():
        discount = dialog_manager.dialog_data['discount']
    firm_id = None
    if 'firm_id' in dialog_manager.dialog_data.keys():
        firm_id = dialog_manager.dialog_data['firm_id']
    series_data = await series_service.update_series(series_id=series_id, title=title,
                                                     description=description, discount=discount, firm_id=firm_id)
    dialog_manager.start_data['series_id'] = series_data.series_id
    await dialog_manager.switch_to(Series.series)


series_update_button = Button(
    text=Const(LEXICON["update_series"]),
    id="series_update",
    on_click=series_update_getter
)


async def series_delete_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    series_id = dialog_manager.dialog_data['series_id']
    logger.info(series_id)
    res = await series_service.delete_series(series_id)
    if 'title' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('title')
    if 'description' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('description')
    if 'discount' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('discount')
    await dialog_manager.switch_to(Series.series_list)


series_delete_button = Button(
    text=Const(LEXICON["delete_series"]),
    id="series_delete",
    on_click=series_delete_button
)


series_update_window = Window(
    Const(LEXICON["update_series"]),
    Group(
        series_update_filter_firms_list_param_button,
        series_update_title_button,
        series_update_description_button,
        series_update_discount_button,
        series_update_button,
        series_delete_button,
        Back(Const(LEXICON["back"])),
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Series.series_update
)

update_series_windows = [series_update_window, series_update_title_window, series_update_description_window,
                         series_update_discount_window, series_update_firms_window]
