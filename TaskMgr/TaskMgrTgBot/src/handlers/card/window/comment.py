from typing import Dict

from aiogram import html
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const, List

from src.lexicon import LEXICON
from src.services import ProjectService, UserService, RoleService, CardService
from src.states.states import Card
from src.handlers.card.window.to_card_button import to_card_button

project_service = ProjectService()
card_service = CardService()
user_service = UserService()
role_service = RoleService()


def add_comment_include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data["card_actions"]
    for action in actions:
        if action[0] == "add_comment_card":
            return True
    return False


async def add_comment_on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.switch_to(Card.add_comment)

add_comment_button = Button(
    text=Const(LEXICON["add"]),
    id="add_comment_card_button",
    when=add_comment_include_button,
    on_click=add_comment_on_click_button
)


async def add_comment_request(message: Message, message_input: MessageInput, manager: DialogManager, **kwargs):
    card_id = int(manager.start_data["card_id"])
    await card_service.create_comment(telegram_id=str(message.from_user.id), card_id=card_id, description=message.text)
    await manager.switch_to(Card.comments)


add_comment_window = Window(
    Const(LEXICON["add"]),
    Const(LEXICON["add_message"]),
    MessageInput(add_comment_request),
    state=Card.add_comment
)


def include_button(data: Dict, widget: Whenable, manager: DialogManager):
    actions = manager.dialog_data["card_actions"]
    for action in actions:
        if action[0] == "get_comment_card":
            return True
    return False


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.answer(text=LEXICON["loading"])
    await manager.switch_to(Card.comments)


async def getter(dialog_manager: DialogManager, **kwargs):
    card_id = int(dialog_manager.start_data["card_id"])

    comments_data = await card_service.comments(card_id=card_id)
    comments = []
    for comment in comments_data:
        user = await user_service.get_user(comment.user_id)
        comments.append(
            f"{html.link(user.name, link=f'tg://user?id={user.telegram_id}')}\n{comment.description}"
        )
    return {
        "comments": comments
    }


comments_button = Button(
    text=Const(LEXICON["comments"]),
    on_click=on_click_button,
    id="comments_button",
    when=include_button
)

comment_card_window = Window(
    Const(LEXICON["comments"]),
    List(
        Format("{item}"),
        items="comments"
    ),
    add_comment_button,
    to_card_button,
    getter=getter,
    state=Card.comments,
)

comment_card_windows = [comment_card_window, add_comment_window]
