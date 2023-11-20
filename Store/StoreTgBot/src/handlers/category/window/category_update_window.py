import operator
import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import CategoryService
from src.states.states import Category

category_service = CategoryService()
logger = logging.getLogger()


async def category_update_go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.category_update)


category_update_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="categories_update_go_back",
    on_click=category_update_go_back_button
)


async def category_update_title_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.category_update_title)


async def category_update_title(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['title'] = message.text
    await dialog_manager.switch_to(Category.category_update)


category_update_title_button = Button(
    text=Const(LEXICON["update_title"]),
    id="categories_update_filter_title",
    on_click=category_update_title_button
)

category_update_title_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(category_update_title),
    Row(category_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.category_update_title
)


async def category_update_description_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.category_update_description)


async def category_update_description(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['description'] = message.text
    await dialog_manager.switch_to(Category.category_update)


category_update_description_button = Button(
    text=Const(LEXICON["update_description"]),
    id="categories_search_filter_description",
    on_click=category_update_description_button
)

category_update_description_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(category_update_description),
    Row(category_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.category_update_description
)


async def category_update_discount_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.category_update_discount)


async def category_update_discount(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data['discount'] = float(message.text)
    await dialog_manager.switch_to(Category.category_update)


category_update_discount_button = Button(
    text=Const(LEXICON["update_discount"]),
    id="categories_search_filter_discount",
    on_click=category_update_discount_button
)

category_update_discount_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(category_update_discount),
    Row(category_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Category.category_update_discount
)


async def category_update_getter(callback: CallbackQuery, button: Button, dialog_dialog_manager: DialogManager, **kwargs):
    category_id = dialog_dialog_manager.dialog_data['category_id']
    title = None
    if 'title' in dialog_dialog_manager.dialog_data.keys():
        title = dialog_dialog_manager.dialog_data['title']
    description = None
    if 'description' in dialog_dialog_manager.dialog_data.keys():
        description = dialog_dialog_manager.dialog_data['description']
    discount = None
    if 'discount' in dialog_dialog_manager.dialog_data.keys():
        discount = dialog_dialog_manager.dialog_data['discount']
    category_data = await category_service.update_category(category_id=category_id, title=title,
                                                           description=description, discount=discount)
    dialog_dialog_manager.start_data['category_id'] = category_data.category_id
    await dialog_dialog_manager.switch_to(Category.category)


category_update_button = Button(
    text=Const(LEXICON["update_category"]),
    id="category_update",
    on_click=category_update_getter
)


async def category_delete_button(callback: CallbackQuery, button: Button, dialog_dialog_manager: DialogManager, **kwargs):
    category_id = dialog_dialog_manager.dialog_data['category_id']
    logger.info(category_id)
    res = await category_service.delete_category(category_id)
    logger.info(res)
    if 'title' in dialog_dialog_manager.dialog_data.keys():
        dialog_dialog_manager.dialog_data.pop('title')
    if 'description' in dialog_dialog_manager.dialog_data.keys():
        dialog_dialog_manager.dialog_data.pop('description')
    if 'discount' in dialog_dialog_manager.dialog_data.keys():
        dialog_dialog_manager.dialog_data.pop('discount')
    await dialog_dialog_manager.switch_to(Category.categories)


category_delete_button = Button(
    text=Const(LEXICON["delete_category"]),
    id="category_delete",
    on_click=category_delete_button
)


category_update_window = Window(
    Const(LEXICON["update_category"]),
    Group(
        category_update_title_button,
        category_update_description_button,
        category_update_discount_button,
        category_update_button,
        category_delete_button,
        Back(Const(LEXICON["back"])),
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Category.category_update
)

update_category_windows = [category_update_window, category_update_title_window, category_update_description_window,
                           category_update_discount_window]
