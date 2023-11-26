import operator
import logging

from typing import Any
from aiogram import html
from aiogram.types import CallbackQuery, Message
from datetime import date

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Calendar
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import OrderService
from src.states.states import Order

order_service = OrderService()
logging = logging.getLogger()


async def orders_history_getter(dialog_manager: DialogManager, **kwargs):
    orders_data = await order_service.orders(tg_id=str(dialog_manager.event.from_user.id), finished=True)
    data = [
        (order.card_id, order.order_id, order.price) for order in orders_data
    ]
    return {
        "orders": data
    }


async def get_card_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data["order_id"] = int(item_id)
    dialog_manager.dialog_data["order_id"] = int(item_id)
    await dialog_manager.switch_to(Order.order_card)


async def card_getter(dialog_manager: DialogManager, **kwargs):
    order_id = int(dialog_manager.dialog_data['order_id'])
    card_data = await order_service.order_card(
        order_id=order_id,
        tg_id=str(dialog_manager.event.from_user.id))
    return {
        "title": card_data.card.title,
        "description": card_data.card.description,
        "due": card_data.card.due,
        "complete": card_data.card.complete,
        "created": card_data.card.created,
    }


order_card_window = Window( # TODO
    Format(html.bold(html.quote("{title}"))),
    Format(html.quote("{description}")),
    Cancel(Const(LEXICON["complete"])),
    state=Order.order_card,
    getter=card_getter
)


orders_history_window = Window(
    Const(LEXICON["orders_history"]),
    ScrollingGroup(
        Select(
            text=Format("{item[1]} - {item[2]} руб."),
            item_id_getter=operator.itemgetter(1),
            items="orders",
            id="order_i",
            on_click=get_card_button
        ),
        id="order_history_group",
        width=1,
        height=10,
    ),
    Cancel(Const(LEXICON["ok"])),
    state=Order.orders_history,
    getter=orders_history_getter
)

orders_history_windows = [order_card_window, orders_history_window]
