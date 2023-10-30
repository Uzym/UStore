from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandObject
from magic_filter import F
from aiogram.fsm.context import FSMContext

from src.keyboards.keyboards import create_action_keyboard
from src.keyboards.section import create_section_action_keyboard
from src.keyboards.card import create_cards_keyboard
from src.keyboards.user import create_users_keyboard, create_select_user_role_keyboard
from src.lexicon import LEXICON
from src.services import ProjectService, UserService, RoleService, SectionService, CardService
from src.filters.callback import ProjectCallback, AddUserCallback, SectionCallback, FormCallback
from src.services.section_service import parse_link_section
from src.states.states import AddUserForm, AddSectionForm, UpdateProjectForm

router: Router = Router()


@router.callback_query(SectionCallback.filter(F.action == "get"))
async def get_section(
        callback: CallbackQuery,
        callback_data: SectionCallback,
        section_service: SectionService
):
    await callback.answer(text=LEXICON["loading"])
    try:
        response = await section_service.get_section(
            section_id=int(callback_data.value),
            telegram_id=str(callback.from_user.id)
        )
        keyboard = create_action_keyboard(
            obj="section",
            callback_factory=SectionCallback,
            parser=parse_link_section,
            links=response.links
        )
        await callback.message.answer(
            text=str(response.section),
            reply_markup=keyboard
        )

    except:
        await callback.answer(text=LEXICON["not_found"])


@router.callback_query(SectionCallback.filter(F.action == "update"))
async def update_section(
        callback: CallbackQuery,
        callback_data: SectionCallback,
        section_service: SectionService
):
    await callback.answer(text=LEXICON["loading"])
    try:
        pass

    except:
        await callback.answer(text=LEXICON["not_found"])


@router.callback_query(SectionCallback.filter(F.action == "add_card"))
async def start_add_card(
        callback: CallbackQuery,
        callback_data: SectionCallback,
        section_service: SectionService
):
    await callback.answer(text=LEXICON["loading"])
    try:
        pass

    except:
        await callback.answer(text=LEXICON["not_found"])


@router.callback_query(SectionCallback.filter(F.action == "get_card"))
async def get_cards(
        callback: CallbackQuery,
        callback_data: SectionCallback,
        section_service: SectionService,
        card_service: CardService
):
    await callback.answer(text=LEXICON["loading"])
    try:
        cards = await section_service.cards(
            section_id=int(callback_data.value),
            telegram_id=str(callback.from_user.id)
        )
        keyboard = create_cards_keyboard(cards)

        await callback.message.answer(
            text=LEXICON["get_cards"],
            reply_markup=keyboard
        )
    except:
        await callback.answer(text=LEXICON["not_found"])

