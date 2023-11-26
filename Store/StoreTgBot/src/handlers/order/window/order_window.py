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
from src.services import OrderService, ProductService
from src.states.states import Order

order_service = OrderService()
product_service = ProductService()
logger = logging.getLogger()


async def order_getter(dialog_manager: DialogManager, **kwargs):
    order = await order_service.orders(tg_id=str(dialog_manager.event.from_user.id), finished=False)
    dialog_manager.dialog_data['order_id'] = order[0].order_id
    order_products_data = await order_service.order_products(tg_id=str(dialog_manager.event.from_user.id),
                                                             order_id=order[0].order_id)
    data = []
    iter = 0
    price = 0
    for order_product in order_products_data:
        iter += 1
        product = await product_service.get_product(product_id=order_product.product_id)
        data.append((product.product_id, iter, order_product.quantity,
                     product.title, product.description, product.cost * order_product.quantity * product.discount,
                     (1 - product.discount) * 100, product.delivery_time))
        price += product.cost * order_product.quantity * product.discount
    return {
        "order_id": order[0].order_id,
        "order_price": price,
        "order_products": data
    }


async def delete_product_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    logger.info(dialog_manager.event.from_user.id)
    logger.info(item_id)
    logger.info(dialog_manager.dialog_data['order_id'])
    await order_service.delete_order_product(tg_id=str(dialog_manager.event.from_user.id),
                                             product_id=int(item_id),
                                             order_id=int(dialog_manager.dialog_data['order_id']))


async def confirm_order_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await order_service.confirm_order(
        tg_id=str(dialog_manager.event.from_user.id),
        order_id=int(dialog_manager.dialog_data['order_id']))
    await dialog_manager.switch_to(Order.orders_history)


confirm_order_button = Button(
    text=Const(LEXICON["confirm_order"]),
    id="confirm_order",
    on_click=confirm_order_button
)


async def delete_order_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await order_service.delete_order(
        tg_id=str(dialog_manager.event.from_user.id),
        order_id=int(dialog_manager.dialog_data['order_id']))
    await dialog_manager.switch_to(Order.orders_history)


delete_order_button = Button(
    text=Const(LEXICON["cancel_order"]),
    id="confirm_order",
    on_click=delete_order_button
)


order_window = Window(
    Const(html.bold(html.quote(LEXICON["order"]))),
    Format(html.bold(html.quote("Номер: {order_id}"))),
    Const("Список продуктов (при нажатии удалит продкут из заказа)"),
    ScrollingGroup(
        Select(
            text=Format("{item[1]}: {item[3]} - {item[2]} шт. Цена: {item[5]} Скидка: {item[6]}%"),
            item_id_getter=operator.itemgetter(0),
            items="order_products",
            id="order_product_i",
            on_click=delete_product_button
        ),
        id="order_products_group",
        width=1,
        height=10,
    ),
    Format(html.quote("Сумма: {order_price} рублей")),
    confirm_order_button,
    delete_order_button,
    Cancel(Const("Выйти")),
    state=Order.order,
    getter=order_getter
)

order_windows = [order_window]
