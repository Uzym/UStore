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
from src.services import OrderService
from src.states.states import Order
from src.handlers.product.window.product_window import get_product_button

order_service = OrderService()
logging = logging.getLogger()


async def orders_getter(dialog_manager: DialogManager, **kwargs):
    orders_data = await order_service.orders(tg_id=str(dialog_manager.event.from_user.id), finished=True)
    data = [
        (order.order_id, order.price) for order in orders_data
    ]
    
