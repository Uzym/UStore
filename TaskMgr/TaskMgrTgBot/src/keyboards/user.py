from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from src.filters.callback import ProjectCallback, AddUserCallback
from aiogram import html
from src.models import domain
from src.services.project_service import parse_link_project
from src.lexicon import LEXICON


def create_users_keyboard(users: list[domain.User], roles: list[str]):
    builder = InlineKeyboardBuilder()
    for idx, user in enumerate(users):
        builder.add(InlineKeyboardButton(
            text=f"{roles[idx]}: {user.name}",
            url=f"tg://user?id={user.telegram_id}"
        ))
        if idx > 20:
            break
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def create_select_user_role_keyboard(obj: str, users: list[domain.User], roles: list[domain.Role]):
    builder = InlineKeyboardBuilder()
    for idx, user in enumerate(users):
        builder.add(InlineKeyboardButton(
            text=f"{user.name} " + LEXICON["add_user_keyboard"],
            url=f"tg://user?id={user.telegram_id}"
        ))
        for jdx, role in enumerate(roles):
            builder.add(InlineKeyboardButton(
                text=f"{role.title}",
                callback_data=AddUserCallback(obj=obj, user_id=user.user_id, role_id=role.role_id).pack()
            ))
        if idx > 10:
            break
    builder.adjust(1, repeat=True)
    return builder.as_markup()