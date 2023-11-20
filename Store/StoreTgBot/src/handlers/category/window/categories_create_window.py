import operator
import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.handlers.firm.window.firm_window import get_firm_button
from src.lexicon import LEXICON
from src.services import CategoryService
from src.states.states import Category

categories_service = CategoryService()
logger = logging.getLogger()


async def category_create_go_back_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Category.category_create)


category_create_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="categories_create_go_back",
    on_click=category_create_go_back_button
)


async def category_create_title_param_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Category.category_create_title_param)


async def category_create_title_param(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['title'] = message.text
    await manager.switch_to(Category.category_create)


category_create_title_param_button = Button(
    text=Const(LEXICON["select_title"]),
    id="categories_search_filter_title",
    on_click=category_create_title_param_button
)


category_create_title_param_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(category_create_title_param),
    Row(category_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.category_create_title_param
)


async def category_create_description_param_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Category.category_create_description_param)


async def category_create_description_param(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['description'] = message.text
    await manager.switch_to(Category.category_create)


category_create_description_param_button = Button(
    text=Const(LEXICON["select_description"]),
    id="categories_search_filter_description",
    on_click=category_create_description_param_button
)


category_create_description_param_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(category_create_description_param),
    Row(category_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.category_create_description_param
)


async def category_create_discount_param_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Category.category_create_discount_param)


async def category_create_discount_param(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['discount'] = float(message.text)
    await manager.switch_to(Category.category_create)


category_create_discount_param_button = Button(
    text=Const(LEXICON["select_discount"]),
    id="categories_search_filter_discount",
    on_click=category_create_discount_param_button
)


category_create_discount_param_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(category_create_discount_param),
    Row(category_create_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.category_create_discount_param
)


async def category_create_getter(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    title = None
    if 'title' in manager.dialog_data.keys():
        title = manager.dialog_data['title']
    description = None
    if 'description' in manager.dialog_data.keys():
        description = manager.dialog_data['description']
    discount = None
    if 'discount' in manager.dialog_data.keys():
        discount = manager.dialog_data['discount']
    category_data = await categories_service.create_category(title=title, description=description, discount=discount)
    manager.start_data['category_id'] = category_data.category_id
    manager.dialog_data['category_id'] = category_data.category_id
    await manager.switch_to(Category.category)


category_create_button = Button(
    text=Const(LEXICON["ok"]),
    id="category_create",
    on_click=category_create_getter
)


category_create_window = Window(
    Const(LEXICON["create_category"]),
    Group(
        category_create_title_param_button,
        category_create_description_param_button,
        category_create_discount_param_button,
        category_create_button,
        category_create_go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Category.category_create
)

create_category_windows = [category_create_title_param_window, category_create_description_param_window,
                           category_create_window, category_create_discount_param_window]
