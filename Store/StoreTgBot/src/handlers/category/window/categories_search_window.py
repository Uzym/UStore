import operator
import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import CategoryService
from src.states.states import Category
from src.handlers.category.window.category_window import get_category_button

category_service = CategoryService()
logging = logging.getLogger()


async def categories_search_go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.categories_search)


categories_search_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="categories_search_go_back",
    on_click=categories_search_go_back_button
)


async def categories_search_filter_title_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                                **kwargs):
    await dialog_manager.switch_to(Category.categories_search_title_filter)


categories_search_filter_title_button = Button(
    text=Const(LEXICON["select_title"]),
    id="categories_search_filter_title",
    on_click=categories_search_filter_title_button
)


async def categories_search_filter_title(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['title'] = message.text
    await dialog_manager.switch_to(Category.categories_search)


categories_search_filter_title_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(categories_search_filter_title),
    Row(categories_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.categories_search_title_filter
)


async def categories_search_filter_description_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                                      **kwargs):
    await dialog_manager.switch_to(Category.categories_search_description_filter)


categories_search_filter_description_button = Button(
    text=Const(LEXICON["select_description"]),
    id="categories_search_filter_description",
    on_click=categories_search_filter_description_button
)


async def categories_search_filter_description(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['description'] = message.text
    await dialog_manager.switch_to(Category.categories_search)


categories_search_filter_description_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(categories_search_filter_description),
    Row(categories_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.categories_search_description_filter
)


async def categories_search_filter_discount_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                                                   **kwargs):
    await dialog_manager.switch_to(Category.categories_search_discount_filter)


categories_search_filter_discount_button = Button(
    text=Const(LEXICON["select_discount"]),
    id="categories_search_filter_discount",
    on_click=categories_search_filter_discount_button
)


async def categories_search_filter_discount(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['discount'] = float(message.text)
    await dialog_manager.switch_to(Category.categories_search)


categories_search_filter_discount_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(categories_search_filter_discount),
    Row(categories_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.categories_search_discount_filter
)


async def categories_search(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    await dialog_manager.switch_to(Category.categories)


categories_search_button = Button(
    text=Const(LEXICON["ok"]),
    id="categories_search",
    on_click=categories_search
)


categories_search_window = Window(
    Const(LEXICON["search_categories"]),
    Group(
        categories_search_filter_title_button,
        categories_search_filter_description_button,
        categories_search_filter_discount_button,
        categories_search_button,
        categories_search_go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Category.categories_search
)


async def categories_getter(dialog_manager: DialogManager, **kwargs):
    title = None
    if 'title' in dialog_manager.dialog_data.keys():
        title = dialog_manager.dialog_data['title']
    description = None
    if 'description' in dialog_manager.dialog_data.keys():
        description = dialog_manager.dialog_data['description']
    discount = None
    if 'discount' in dialog_manager.dialog_data.keys():
        discount = dialog_manager.dialog_data['discount']
    categories_data = await category_service.categories(title=title, description=description, discount=discount)
    data = [
        (category.title, str(category.category_id)) for category in categories_data
    ]
    return {
        "categories": data
    }


categories_window = Window(
    Const(LEXICON["categories_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="categories",
            id="category_i",
            on_click=get_category_button
        ),
        id="categories_group",
        width=1,
        height=10,
    ),
    categories_search_go_back_button,
    Cancel(Const(LEXICON["ok"])),
    state=Category.categories,
    getter=categories_getter
)

search_category_windows = [categories_search_filter_title_window, categories_search_filter_description_window,
                           categories_search_filter_discount_window, categories_search_window, categories_window]
