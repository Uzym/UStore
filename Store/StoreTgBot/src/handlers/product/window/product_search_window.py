import operator
import logging

from typing import Any
from aiogram.types import CallbackQuery, Message
from datetime import date

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Calendar
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import ProductService, SeriesService, FirmService, CategoryService
from src.states.states import Product
from src.handlers.product.window.product_window import get_product_button

product_service = ProductService()
series_service = SeriesService()
firm_service = FirmService()
category_service = CategoryService()
logging = logging.getLogger()


async def products_search_go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.products_search)


products_search_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="products_search_go_back",
    on_click=products_search_go_back_button
)


async def products_search_filter_firms_list_button(callback: CallbackQuery, button: Button,
                                                   dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.products_search_firms_list)


products_search_filter_firms_list_button = Button(
    text=Const(LEXICON["select_firm"]),
    id="products_search_filter_firms_list",
    on_click=products_search_filter_firms_list_button
)


async def products_search_filter_firm_id_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                                item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data['firm_id'] = int(item_id)
    dialog_manager.dialog_data['firm_id'] = int(item_id)
    await dialog_manager.switch_to(Product.products_search)


async def products_search_firms_getter(dialog_manager: DialogManager, **kwargs):
    firms_data = await firm_service.firms()
    data = [
        (firm.title, str(firm.firm_id)) for firm in firms_data
    ]
    return {
        "firms": data
    }


products_search_firms_window = Window(
    Const(LEXICON["firms_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="firms",
            id="firm_i",
            on_click=products_search_filter_firm_id_button
        ),
        id="firms_group",
        width=1,
        height=10,
    ),
    products_search_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Product.products_search_firms_list,
    getter=products_search_firms_getter
)


async def products_search_filter_categories_list_button(callback: CallbackQuery, button: Button,
                                                        dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.products_search_categories_list)


products_search_filter_categories_list_button = Button(
    text=Const(LEXICON["select_category"]),
    id="products_search_filter_categories_list",
    on_click=products_search_filter_categories_list_button
)


async def products_search_filter_category_id_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                                    item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data['category_id'] = int(item_id)
    dialog_manager.dialog_data['category_id'] = int(item_id)
    await dialog_manager.switch_to(Product.products_search)


async def products_search_categories_getter(dialog_manager: DialogManager, **kwargs):
    categories_data = await category_service.categories()
    data = [
        (category.title, str(category.category_id)) for category in categories_data
    ]
    return {
        "categories": data
    }


products_search_categories_window = Window(
    Const(LEXICON["categories_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="categories",
            id="category_i",
            on_click=products_search_filter_category_id_button
        ),
        id="categories_group",
        width=1,
        height=10,
    ),
    products_search_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Product.products_search_categories_list,
    getter=products_search_categories_getter
)


async def products_search_filter_series_list_button(callback: CallbackQuery, button: Button,
                                                    dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.products_search_series_list)


products_search_filter_series_list_button = Button(
    text=Const(LEXICON["select_series"]),
    id="products_search_filter_series_list",
    on_click=products_search_filter_series_list_button
)


async def products_search_filter_series_id_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager,
                                                  item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data['series_id'] = int(item_id)
    dialog_manager.dialog_data['series_id'] = int(item_id)
    await dialog_manager.switch_to(Product.products_search)


async def products_search_series_getter(dialog_manager: DialogManager, **kwargs):
    series_data = await series_service.series_list()
    data = [
        (series.title, str(series.series_id)) for series in series_data
    ]
    return {
        "series_list": data
    }


products_search_series_window = Window(
    Const(LEXICON["series_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="series_list",
            id="series_i",
            on_click=products_search_filter_series_id_button
        ),
        id="series_group",
        width=1,
        height=10,
    ),
    products_search_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Product.products_search_series_list,
    getter=products_search_series_getter
)


async def products_search_filter_title_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                              **kwargs):
    await dialog_manager.switch_to(Product.products_search_title_filter)


products_search_filter_title_button = Button(
    text=Const(LEXICON["select_title"]),
    id="products_search_filter_title",
    on_click=products_search_filter_title_button
)


async def products_search_filter_title(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['title'] = message.text
    await dialog_manager.switch_to(Product.products_search)


products_search_filter_title_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(products_search_filter_title),
    Row(products_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.products_search_title_filter
)


async def products_search_filter_description_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                                    **kwargs):
    await dialog_manager.switch_to(Product.products_search_description_filter)


products_search_filter_description_button = Button(
    text=Const(LEXICON["select_description"]),
    id="products_search_filter_description",
    on_click=products_search_filter_description_button
)


async def products_search_filter_description(message: Message, message_input: MessageInput,
                                             dialog_manager: DialogManager):
    dialog_manager.dialog_data['description'] = message.text
    await dialog_manager.switch_to(Product.products_search)


products_search_filter_description_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(products_search_filter_description),
    Row(products_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.products_search_description_filter
)


async def products_search_filter_discount_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                                 **kwargs):
    await dialog_manager.switch_to(Product.products_search_discount_filter)


products_search_filter_discount_button = Button(
    text=Const(LEXICON["select_discount"]),
    id="products_search_filter_discount",
    on_click=products_search_filter_discount_button
)


async def products_search_filter_discount(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['discount'] = float(message.text)
    await dialog_manager.switch_to(Product.products_search)


products_search_filter_discount_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(products_search_filter_discount),
    Row(products_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.products_search_discount_filter
)


async def products_search_filter_cost_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                              **kwargs):
    await dialog_manager.switch_to(Product.products_search_cost_filter)


products_search_filter_cost_button = Button(
    text=Const(LEXICON["select_cost"]),
    id="products_search_filter_cost",
    on_click=products_search_filter_cost_button
)


async def products_search_filter_cost(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['cost'] = float(message.text)
    await dialog_manager.switch_to(Product.products_search)


products_search_filter_cost_window = Window(
    Const(LEXICON["input_cost"]),
    MessageInput(products_search_filter_cost),
    Row(products_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.products_search_cost_filter
)


async def products_search_filter_delivery_time_button(callback: CallbackQuery, button: Button,
                                                      dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.products_search_delivery_time_filter)


products_search_filter_delivery_time_button = Button(
    text=Const(LEXICON["select_delivery_time"]),
    id="products_search_filter_delivery_time",
    on_click=products_search_filter_delivery_time_button
)


async def products_search_filter_delivery_time(message: Message, message_input: MessageInput,
                                               dialog_manager: DialogManager):
    dialog_manager.dialog_data['delivery_time'] = message.text
    await dialog_manager.switch_to(Product.products_search)


products_search_filter_delivery_time_window = Window(
    Const(LEXICON["input_delivery_time"]),
    MessageInput(products_search_filter_delivery_time),
    Row(products_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Product.products_search_delivery_time_filter
)


async def products_search(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Product.products)


products_search_button = Button(
    text=Const(LEXICON["ok"]),
    id="products_search",
    on_click=products_search
)


products_search_window = Window(
    Const(LEXICON["search_products"]),
    Group(
        products_search_filter_categories_list_button,
        products_search_filter_firms_list_button,
        products_search_filter_series_list_button,
        products_search_filter_title_button,
        products_search_filter_description_button,
        products_search_filter_discount_button,
        products_search_filter_cost_button,
        products_search_filter_delivery_time_button,
        products_search_button,
        products_search_go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Product.products_search
)


async def products_getter(dialog_manager: DialogManager, **kwargs):
    firm_id = None
    if 'firm_id' in dialog_manager.dialog_data.keys():
        firm_id = dialog_manager.dialog_data['firm_id']
    category_id = None
    if 'category_id' in dialog_manager.dialog_data.keys():
        category_id = dialog_manager.dialog_data['category_id']
    series_id = None
    if 'series_id' in dialog_manager.dialog_data.keys():
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
    cost = None
    if 'cost' in dialog_manager.dialog_data.keys():
        cost = dialog_manager.dialog_data['cost']
    delivery_time = None
    if 'delivery_time' in dialog_manager.dialog_data.keys():
        delivery_time = dialog_manager.dialog_data['delivery_time']
    products_data = await product_service.products(firm_id=firm_id, series_id=series_id, category_id=category_id, 
                                                   title=title, description=description, discount=discount, cost=cost, 
                                                   delivery_time=delivery_time)
    data = [
        (product.title, str(product.product_id)) for product in products_data
    ]
    return {
        "products": data
    }


products_window = Window(
    Const(LEXICON["products_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="products",
            id="product_i",
            on_click=get_product_button
        ),
        id="products_group",
        width=1,
        height=10,
    ),
    products_search_go_back_button,
    Cancel(Const(LEXICON["ok"])),
    state=Product.products,
    getter=products_getter
)

search_product_windows = [products_search_firms_window, products_search_categories_window,
                          products_search_series_window, products_search_filter_cost_window,
                          products_search_filter_title_window, products_search_filter_description_window,
                          products_search_filter_delivery_time_window, products_search_filter_discount_window,
                          products_search_window, products_window]
