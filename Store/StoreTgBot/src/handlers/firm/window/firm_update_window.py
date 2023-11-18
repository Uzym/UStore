import operator
import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import FirmService
from src.states.states import Firm


firm_service = FirmService()
logger = logging.getLogger()


async def firm_update_go_back_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firm_update)


firm_update_go_back_button = Button(
    text=Const("Назад"),
    id="firms_update_go_back",
    on_click=firm_update_go_back_button
)


async def firm_update_title_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firm_update_title)


async def firm_update_title(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['title'] = message.text
    await manager.switch_to(Firm.firm_update)


firm_update_title_button = Button(
    text=Const("Обновить название"),
    id="firms_update_filter_title",
    on_click=firm_update_title_button
)

firm_update_title_window = Window(
    Const("Введите название фирмы"),
    MessageInput(firm_update_title),
    Row(firm_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Firm.firm_update_title
)


async def firm_update_description_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firm_update_description)


async def firm_update_description(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['description'] = message.text
    await manager.switch_to(Firm.firm_update)


firm_update_description_button = Button(
    text=Const("Обновить описание"),
    id="firms_search_filter_description",
    on_click=firm_update_description_button
)

firm_update_description_window = Window(
    Const("Введите описание фирмы"),
    MessageInput(firm_update_description),
    Row(firm_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Firm.firm_update_description
)


async def firm_update_discount_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firm_update_discount)


async def firm_update_discount(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['discount'] = float(message.text)
    await manager.switch_to(Firm.firm_update)


firm_update_discount_button = Button(
    text=Const("Обновить скидку"),
    id="firms_search_filter_discount",
    on_click=firm_update_discount_button
)

firm_update_discount_window = Window(
    Const("Введите скидку"),
    MessageInput(firm_update_discount),
    Row(firm_update_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Firm.firm_update_discount
)


async def firm_update_getter(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    firm_id = dialog_manager.dialog_data['firm_id']
    title = None
    if 'title' in dialog_manager.dialog_data.keys():
        title = dialog_manager.dialog_data['title']
    description = None
    if 'description' in dialog_manager.dialog_data.keys():
        description = dialog_manager.dialog_data['description']
    discount = None
    if 'discount' in dialog_manager.dialog_data.keys():
        discount = dialog_manager.dialog_data['discount']
    firm_data = await firm_service.update_firm(firm_id=firm_id, title=title, description=description, discount=discount)
    dialog_manager.start_data['firm_id'] = firm_data.firm_id
    await dialog_manager.switch_to(Firm.firm)


firm_update_button = Button(
    text=Const("Изменить фирму"),
    id="firm_update",
    on_click=firm_update_getter
)


async def firm_delete_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    firm_id = dialog_manager.dialog_data['firm_id']
    logger.info(firm_id)
    res = await firm_service.delete_firm(firm_id)
    logger.info(res)
    if 'title' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('title')
    if 'description' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('description')
    if 'discount' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('discount')
    await dialog_manager.switch_to(Firm.firms)


firm_delete_button = Button(
    text=Const("Удалить фирму"),
    id="firm_delete",
    on_click=firm_delete_button
)


firm_update_window = Window(
    Const("Изменить фирму"),
    Group(
        firm_update_title_button,
        firm_update_description_button,
        firm_update_discount_button,
        firm_update_button,
        firm_delete_button,
        Back(Const(LEXICON["back"])),
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Firm.firm_update
)

update_firm_windows = [firm_update_window, firm_update_title_window, firm_update_description_window,
                       firm_update_discount_window]
