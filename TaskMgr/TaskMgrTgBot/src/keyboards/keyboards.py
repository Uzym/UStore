from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder, InlineKeyboardMarkup
from src.filters.callback import SectionCallback, FormCallback
from aiogram import html
from src.models import domain
from src.services.section_service import parse_link_section
from src.lexicon import LEXICON


def create_action_keyboard(obj: str, links: list[domain.Link], parser, callback_factory) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for idx, link in enumerate(links):
        ids, action, values_include = parser(link)
        # if not action[0:3] == "get":
        #     builder.add(InlineKeyboardButton(
        #         text=LEXICON[action + f"_{obj}"],
        #         callback_data=FormCallback(obj=obj, tag=action, cnt=values_include)
        #     ))
        # else:
        builder.add(InlineKeyboardButton(
            text=LEXICON[action + f"_{obj}"],
            callback_data=callback_factory(action=action, value=ids).pack()
        ))
        if idx > 20:
            break
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def create_get_objects_keyboard(data: list[tuple], callback_factory) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for idx, obj in enumerate(data):
        builder.add(InlineKeyboardButton(
            text=f"{idx}: {obj[0]}",
            callback_data=callback_factory(action="get", value=obj[1]).pack()
        ))
        if idx > 20:
            break
    builder.adjust(1, repeat=True)
    return builder.as_markup()
