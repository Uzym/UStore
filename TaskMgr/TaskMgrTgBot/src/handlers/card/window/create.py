from datetime import datetime

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from src.lexicon import LEXICON
from src.services import SectionService, CardService, RoleService, UserService
from src.states.states import Card

section_service = SectionService()
card_service = CardService()
role_service = RoleService()
user_service = UserService()


async def on_click_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    try:
        section_id = int(manager.start_data["section_id"])
        title = f"Карточка {str(callback.from_user.full_name)} от {str(datetime.now())}"
        card = await section_service.create_card(
            telegram_id=str(callback.from_user.id),
            section_id=section_id,
            title=title
        )
        user = await user_service.users(telegram_id=str(callback.from_user.id))
        role = await role_service.roles(description="telegram creator card role")
        await card_service.add_user(card_id=card.card_id, user_id=user[0].user_id, role_id=role[0].role_id)

        manager.start_data["card_id"] = str(card.card_id)
        manager.start_data["update_card_visible"] = True
        await manager.start(
            Card.card,
            data=manager.start_data
        )
    except:
        manager.dialog_data['user_name'] = LEXICON["not_found"]


create_card_button = Button(
    text=Const(LEXICON["add"]),
    id="create_card_button",
    on_click=on_click_button,
)
