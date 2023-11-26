import operator
import logging

from aiogram.types import CallbackQuery, Message
from typing import Any

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.handlers.firm.window.firm_window import get_firm_button
from src.lexicon import LEXICON
from src.services import ProductService, CategoryService, SeriesService
from src.states.states import Product

product_service = ProductService()
category_service = CategoryService()
series_service = SeriesService()
logger = logging.getLogger()


async def product_create_go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Product.product_create)


product_create_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="products_create_go_back",
    on_click=product_create_go_back_button
)


async def product_create_categories_list_param_button(callback: CallbackQuery, button: Button,
                                                      dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.product_create_categories_list)


product_create_filter_categories_list_param_button = Button(
    text=Const(LEXICON["select_category"]),
    id="product_create_categories_list_param",
    on_click=product_create_categories_list_param_button
)


async def product_create_category_id_param_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                                  item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data['category_id'] = int(item_id)
    dialog_manager.dialog_data['category_id'] = int(item_id)
    await dialog_manager.switch_to(Product.product_create)


async def product_create_categories_getter(dialog_manager: DialogManager, **kwargs):
    categories_data = await category_service.categories()
    data = [
        (category.title, str(category.category_id)) for category in categories_data
    ]
    return {
        "categories": data
    }


product_create_categories_window = Window(
    Const(LEXICON["categories_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="categories",
            id="category_i",
            on_click=product_create_category_id_param_button
        ),
        id="categories_group",
        width=1,
        height=10,
    ),
    product_create_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Product.product_create_categories_list,
    getter=product_create_categories_getter
)


async def product_create_series_list_param_button(callback: CallbackQuery, button: Button,
                                                  dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.product_create_series_list)


product_create_filter_series_list_param_button = Button(
    text=Const(LEXICON["select_series"]),
    id="product_create_series_list_param",
    on_click=product_create_series_list_param_button
)


async def product_create_series_id_param_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                                item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data['series_id'] = int(item_id)
    dialog_manager.dialog_data['series_id'] = int(item_id)
    await dialog_manager.switch_to(Product.product_create)


async def product_create_series_getter(dialog_manager: DialogManager, **kwargs):
    series_data = await series_service.series_list()
    data = [
        (series.title, str(series.series_id)) for series in series_data
    ]
    return {
        "series": data
    }


product_create_series_window = Window(
    Const(LEXICON["series_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="series",
            id="series_i",
            on_click=product_create_series_id_param_button
        ),
        id="series_group",
        width=1,
        height=10,
    ),
    product_create_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Product.product_create_series_list,
    getter=product_create_series_getter
)


async def product_create_title_param_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Product.product_create_title_param)


async def product_create_title_param(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['title'] = message.text
    await dialog_manager.switch_to(Product.product_create)


product_create_title_param_button = Button(
    text=Const(LEXICON["select_title"]),
    id="products_search_filter_title",
    on_click=product_create_title_param_button
)


product_create_title_param_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(product_create_title_param),
    Row(product_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.product_create_title_param
)


async def product_create_description_param_button(callback: CallbackQuery, button: Button,
                                                  dialog_manager: DialogManager):
    await dialog_manager.switch_to(Product.product_create_description_param)


async def product_create_description_param(message: Message, message_input: MessageInput,
                                           dialog_manager: DialogManager):
    dialog_manager.dialog_data['description'] = message.text
    await dialog_manager.switch_to(Product.product_create)


product_create_description_param_button = Button(
    text=Const(LEXICON["select_description"]),
    id="products_search_filter_description",
    on_click=product_create_description_param_button
)


product_create_description_param_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(product_create_description_param),
    Row(product_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.product_create_description_param
)


async def product_create_discount_param_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Product.product_create_discount_param)


async def product_create_discount_param(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['discount'] = float(message.text)
    await dialog_manager.switch_to(Product.product_create)


product_create_discount_param_button = Button(
    text=Const(LEXICON["select_discount"]),
    id="products_search_filter_discount",
    on_click=product_create_discount_param_button
)


product_create_discount_param_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(product_create_discount_param),
    Row(product_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.product_create_discount_param
)


async def product_create_cost_param_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Product.product_create_cost_param)


async def product_create_cost_param(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['cost'] = float(message.text)
    await dialog_manager.switch_to(Product.product_create)


product_create_cost_param_button = Button(
    text=Const(LEXICON["select_cost"]),
    id="products_search_filter_cost",
    on_click=product_create_cost_param_button
)


product_create_cost_param_window = Window(
    Const(LEXICON["input_cost"]),
    MessageInput(product_create_cost_param),
    Row(product_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.product_create_cost_param
)


async def product_create_delivery_time_param_button(callback: CallbackQuery, button: Button,
                                                    dialog_manager: DialogManager):
    await dialog_manager.switch_to(Product.product_create_delivery_time_param)


async def product_create_delivery_time_param(message: Message, message_input: MessageInput,
                                             dialog_manager: DialogManager):
    dialog_manager.dialog_data['delivery_time'] = message.text
    await dialog_manager.switch_to(Product.product_create)


product_create_delivery_time_param_button = Button(
    text=Const(LEXICON["select_delivery_time"]),
    id="products_search_filter_delivery_time",
    on_click=product_create_delivery_time_param_button
)


product_create_delivery_time_param_window = Window(
    Const(LEXICON["input_delivery_time"]),
    MessageInput(product_create_delivery_time_param),
    Row(product_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.product_create_delivery_time_param
)


async def product_create_getter(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    title = None
    if 'title' in dialog_manager.dialog_data.keys():
        title = dialog_manager.dialog_data['title']
    description = None
    if 'description' in dialog_manager.dialog_data.keys():
        description = dialog_manager.dialog_data['description']
    discount = None
    if 'discount' in dialog_manager.dialog_data.keys():
        discount = dialog_manager.dialog_data['discount']
    cost = None
    if 'cost' in dialog_manager.dialog_data.keys():
        cost = dialog_manager.dialog_data['cost']
    delivery_time = None
    if 'delivery_time' in dialog_manager.dialog_data.keys():
        delivery_time = dialog_manager.dialog_data['delivery_time']
    series_id = None
    if 'series_id' in dialog_manager.dialog_data.keys():
        series_id = dialog_manager.dialog_data['series_id']
    category_id = None
    if 'category_id' in dialog_manager.dialog_data.keys():
        category_id = dialog_manager.dialog_data['category_id']
    product_data = await product_service.create_product(title=title, description=description, discount=discount,
                                                        cost=cost, delivery_time=delivery_time, series_id=series_id,
                                                        category_id=category_id)
    logger.info(product_data)
    dialog_manager.start_data['product_id'] = product_data.product_id
    dialog_manager.dialog_data['product_id'] = product_data.product_id
    await dialog_manager.switch_to(Product.product)


product_create_button = Button(
    text=Const(LEXICON["ok"]),
    id="product_create",
    on_click=product_create_getter
)


product_create_window = Window(
    Const(LEXICON["create_product"]),
    Group(
        product_create_filter_categories_list_param_button,
        product_create_filter_series_list_param_button,
        product_create_title_param_button,
        product_create_description_param_button,
        product_create_discount_param_button,
        product_create_cost_param_button,
        product_create_delivery_time_param_button,
        product_create_button,
        product_create_go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Product.product_create
)

create_product_windows = [product_create_categories_window, product_create_series_window,
                          product_create_title_param_window, product_create_description_param_window,
                          product_create_window, product_create_discount_param_window,
                          product_create_cost_param_window, product_create_delivery_time_param_window]
