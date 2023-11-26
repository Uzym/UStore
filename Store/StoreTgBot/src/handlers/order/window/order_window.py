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


async def order_go_back_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Order.order)


order_go_back_button = Button(
    text=Const(LEXICON["back"]),
    id="order_go_back",
    on_click=order_go_back_button
)


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
    id="delete_order",
    on_click=delete_order_button
)


async def order_comments_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await dialog_manager.switch_to(Order.order_comments)


order_comments_button = Button(
    text=Const(LEXICON["order_comments"]),
    id="order_comments",
    on_click=order_comments_button
)


async def order_comments_getter(dialog_manager: DialogManager, **kwargs):
    order_id = dialog_manager.dialog_data['order_id']
    comments_data = await order_service.order_comments(order_id=order_id)
    data = [
        (comment.comment_id, comment.description) for comment in comments_data
    ]
    return {
        "order_comments": data
    }


async def get_comment_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.dialog_data["description"] = item_id
    await dialog_manager.switch_to(Order.order_comment)


async def comment_getter(dialog_manager: DialogManager, **kwargs):
    return {
        "description": dialog_manager.dialog_data['description']
    }


get_comment_window = Window(
    Const(LEXICON["comment"]),
    Format(html.quote("{description}")),
    order_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Order.order_comment,
    getter=comment_getter
)


async def add_comment_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager,
                             **kwargs):
    await dialog_manager.switch_to(Order.add_comment)


add_comment_button = Button(
    text=Const(LEXICON["add_comment"]),
    id="add_comment",
    on_click=add_comment_button
)


async def add_comment(message: Message, message_input: MessageInput, dialog_manager: DialogManager):

    await order_service.add_comment(description=message.text, order_id=dialog_manager.dialog_data['order_id'])
    await dialog_manager.switch_to(Order.order)


add_comment_window = Window(
    Const(LEXICON["input_comment"]),
    MessageInput(add_comment),
    Row(order_go_back_button, Cancel(Const(LEXICON["cancel"]))),
    state=Order.add_comment
)


order_comments_window = Window(
    Const(LEXICON["order_comments"]),
    ScrollingGroup(
        Select(
            text=Format("{item[1]}"),
            item_id_getter=operator.itemgetter(1),
            items="order_comments",
            id="order_comment_i",
            on_click=get_comment_button
        ),
        id="order_comments_group",
        width=1,
        height=10,
    ),
    add_comment_button,
    order_go_back_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Order.order_comments,
    getter=order_comments_getter
)


order_window = Window(
    Const(html.bold(html.quote(LEXICON["order"]))),
    Format(html.bold(html.quote("Номер: {order_id}"))),
    Const(LEXICON["order_products_list"]),
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
    order_comments_button,
    confirm_order_button,
    delete_order_button,
    Cancel(Const(LEXICON["cancel"])),
    state=Order.order,
    getter=order_getter
)

order_windows = [order_window, order_comments_window, get_comment_window, add_comment_window]
