from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from src.filters.callback import SectionCallback
from aiogram import html
from src.models import domain
from src.services.section_service import parse_link_section
from src.lexicon import LEXICON


def create_cards_keyboard(cards: list[domain.Card]):
    builder = InlineKeyboardBuilder()
    for idx, card in enumerate(cards):
        builder.add(InlineKeyboardButton(
            text=f"{idx}: {card.title}",
            callback_data=SectionCallback(action="get", value=card.card_id).pack()
        ))
        if idx > 30:
            break
    builder.adjust(1, repeat=True)
    return builder.as_markup()


# def create_section_action_keyboard(links: list[domain.Link]):
#     builder = InlineKeyboardBuilder()
#     for idx, link in enumerate(links):
#         section_id, action = parse_link_section(link)
#         builder.add(InlineKeyboardButton(
#             text=LEXICON[action + "_section"],
#             callback_data=SectionCallback(action=action, value=section_id).pack()
#         ))
#         if idx > 20:
#             break
#     builder.adjust(1, repeat=True)
#     return builder.as_markup()
#
#
