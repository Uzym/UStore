import operator
import logging

from typing import Any
from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import SeriesService, FirmService, CategoryService
from src.states.states import Series
from src.handlers.series.window.series_window import get_series_button

series_service = SeriesService()
firm_service = FirmService()
category_service = CategoryService()
logging = logging.getLogger()


async def series_search_go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Series.series_search)


series_search_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="series_search_go_back",
    on_click=series_search_go_back_button
)


async def series_search_filter_firms_list_button(callback: CallbackQuery, button: Button,
                                                 dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Series.series_search_firms_list)


series_search_filter_firms_list_button = Button(
    text=Const(LEXICON["select_firm"]),
    id="series_search_filter_firms_list",
    on_click=series_search_filter_firms_list_button
)


async def series_search_filter_firm_id_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                              item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data['firm_id'] = int(item_id)
    dialog_manager.dialog_data['firm_id'] = int(item_id)
    await dialog_manager.switch_to(Series.series_search)


async def series_search_firms_getter(dialog_manager: DialogManager, **kwargs):
    firms_data = await firm_service.firms()
    data = [
        (firm.title, str(firm.firm_id)) for firm in firms_data
    ]
    return {
        "firms": data
    }


series_search_firms_window = Window(
    Const(LEXICON["firms_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="firms",
            id="firm_i",
            on_click=series_search_filter_firm_id_button
        ),
        id="firms_group",
        width=1,
        height=10,
    ),
    series_search_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Series.series_search_firms_list,
    getter=series_search_firms_getter
)


async def series_search_filter_categories_list_button(callback: CallbackQuery, button: Button,
                                                      dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Series.series_search_categories_list)


series_search_filter_categories_list_button = Button(
    text=Const(LEXICON["select_category"]),
    id="series_search_filter_firms_list",
    on_click=series_search_filter_categories_list_button
)


async def series_search_filter_category_id_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                                  item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data['category_id'] = int(item_id)
    dialog_manager.dialog_data['category_id'] = int(item_id)
    await dialog_manager.switch_to(Series.series_search)


async def series_search_categories_getter(dialog_manager: DialogManager, **kwargs):
    categories_data = await category_service.categories()
    data = [
        (category.title, str(category.category_id)) for category in categories_data
    ]
    return {
        "categories": data
    }


series_search_categories_window = Window(
    Const(LEXICON["categories_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="categories",
            id="category_i",
            on_click=series_search_filter_category_id_button
        ),
        id="categories_group",
        width=1,
        height=10,
    ),
    series_search_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Series.series_search_categories_list,
    getter=series_search_categories_getter
)


async def series_search_filter_title_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                            **kwargs):
    await dialog_manager.switch_to(Series.series_search_title_filter)


series_search_filter_title_button = Button(
    text=Const(LEXICON["select_title"]),
    id="series_search_filter_title",
    on_click=series_search_filter_title_button
)


async def series_search_filter_title(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['title'] = message.text
    await dialog_manager.switch_to(Series.series_search)


series_search_filter_title_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(series_search_filter_title),
    Row(series_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_search_title_filter
)


async def series_search_filter_description_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                                  **kwargs):
    await dialog_manager.switch_to(Series.series_search_description_filter)


series_search_filter_description_button = Button(
    text=Const(LEXICON["select_description"]),
    id="series_search_filter_description",
    on_click=series_search_filter_description_button
)


async def series_search_filter_description(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['description'] = message.text
    await dialog_manager.switch_to(Series.series_search)


series_search_filter_description_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(series_search_filter_description),
    Row(series_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_search_description_filter
)


async def series_search_filter_discount_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                               **kwargs):
    await dialog_manager.switch_to(Series.series_search_discount_filter)


series_search_filter_discount_button = Button(
    text=Const(LEXICON["select_discount"]),
    id="series_search_filter_discount",
    on_click=series_search_filter_discount_button
)


async def series_search_filter_discount(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['discount'] = float(message.text)
    await dialog_manager.switch_to(Series.series_search)


series_search_filter_discount_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(series_search_filter_discount),
    Row(series_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Series.series_search_discount_filter
)


async def series_search(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Series.series_list)


series_search_button = Button(
    text=Const(LEXICON["ok"]),
    id="series_search",
    on_click=series_search
)

series_search_window = Window(
    Const(LEXICON["search_series"]),
    Group(
        series_search_filter_firms_list_button,
        series_search_filter_categories_list_button,
        series_search_filter_title_button,
        series_search_filter_description_button,
        series_search_filter_discount_button,
        series_search_button,
        series_search_go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Series.series_search
)


async def series_getter(dialog_manager: DialogManager, **kwargs):
    title = None
    if 'title' in dialog_manager.dialog_data.keys():
        title = dialog_manager.dialog_data['title']
    description = None
    if 'description' in dialog_manager.dialog_data.keys():
        description = dialog_manager.dialog_data['description']
    discount = None
    if 'discount' in dialog_manager.dialog_data.keys():
        discount = dialog_manager.dialog_data['discount']
    series_data = await series_service.series_list(title=title, description=description, discount=discount)
    data = [
        (series.title, str(series.series_id)) for series in series_data
    ]
    return {
        "series": data
    }


series_window = Window(
    Const(LEXICON["series_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="series",
            id="series_i",
            on_click=get_series_button
        ),
        id="series_group",
        width=1,
        height=10,
    ),
    series_search_go_back_button,
    Cancel(Const(LEXICON["ok"])),
    state=Series.series_list,
    getter=series_getter
)

search_series_windows = [series_search_firms_window, series_search_categories_window,
                         series_search_filter_title_window, series_search_filter_description_window,
                         series_search_filter_discount_window, series_search_window, series_window]
