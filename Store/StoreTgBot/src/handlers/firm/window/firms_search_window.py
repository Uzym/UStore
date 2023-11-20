import operator
import logging

from aiogram.types import CallbackQuery, Message

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import FirmService
from src.states.states import Firm
from src.handlers.firm.window.firm_window import get_firm_button


firm_service = FirmService()
logger = logging.getLogger()


async def firms_search_go_back_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firms_search)


firms_search_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="firms_search_go_back",
    on_click=firms_search_go_back_button
)


async def firms_search_filter_title_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firms_search_title_filter)


async def firms_search_filter_title(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['title'] = message.text
    await manager.switch_to(Firm.firms_search)


firms_search_filter_title_button = Button(
    text=Const(LEXICON["select_title"]),
    id="firms_search_filter_title",
    on_click=firms_search_filter_title_button
)

firms_search_filter_title_window = Window(
    Const(LEXICON["input_title"]),
    MessageInput(firms_search_filter_title),
    Row(firms_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Firm.firms_search_title_filter
)


async def firms_search_filter_description_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firms_search_description_filter)


async def firms_search_filter_description(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['description'] = message.text
    await manager.switch_to(Firm.firms_search)


firms_search_filter_description_button = Button(
    text=Const(LEXICON["select_description"]),
    id="firms_search_filter_description",
    on_click=firms_search_filter_description_button
)

firms_search_filter_description_window = Window(
    Const(LEXICON["input_description"]),
    MessageInput(firms_search_filter_description),
    Row(firms_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Firm.firms_search_description_filter
)


async def firms_search_filter_discount_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firms_search_discount_filter)


async def firms_search_filter_discount(message: Message, message_input: MessageInput, manager: DialogManager):
    manager.dialog_data['discount'] = float(message.text)  # TODO подсчет скидки переделать в соответствии с ТЗ
    await manager.switch_to(Firm.firms_search)


firms_search_filter_discount_button = Button(
    text=Const(LEXICON["select_discount"]),
    id="firms_search_filter_discount",
    on_click=firms_search_filter_discount_button
)

firms_search_filter_discount_window = Window(
    Const(LEXICON["input_discount"]),
    MessageInput(firms_search_filter_discount),
    Row(firms_search_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Firm.firms_search_discount_filter
)


async def firms_search(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Firm.firms)


firms_search_button = Button(
    text=Const(LEXICON["ok"]),
    id="firms_search",
    on_click=firms_search
)


firms_search_window = Window(
    Const(LEXICON["search_firms"]),
    Group(
        firms_search_filter_title_button,
        firms_search_filter_description_button,
        firms_search_filter_discount_button,
        firms_search_button,
        firms_search_go_back_button,
        Cancel(Const(LEXICON["cancel"]))
    ),
    state=Firm.firms_search,
)


async def firms_getter(dialog_manager: DialogManager, **kwargs):
    title = None
    if 'title' in dialog_manager.dialog_data.keys():
        title = dialog_manager.dialog_data['title']
    description = None
    if 'description' in dialog_manager.dialog_data.keys():
        description = dialog_manager.dialog_data['description']
    discount = None
    if 'discount' in dialog_manager.dialog_data.keys():
        discount = dialog_manager.dialog_data['discount']
    firms_data = await firm_service.firms(title=title, description=description, discount=discount)
    data = [
        (firm.title, str(firm.firm_id)) for firm in firms_data
    ]
    return {
        "firms": data
    }


firms_window = Window(
    Const(LEXICON["firms_list"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="firms",
            id="firm_i",
            on_click=get_firm_button
        ),
        id="firms_group",
        width=1,
        height=10,
    ),
    firms_search_go_back_button,
    Cancel(Const(LEXICON["ok"])),
    state=Firm.firms,
    getter=firms_getter
)


search_firm_windows = [firms_search_filter_title_window, firms_search_filter_description_window,
                       firms_search_filter_discount_window, firms_search_window, firms_window]
