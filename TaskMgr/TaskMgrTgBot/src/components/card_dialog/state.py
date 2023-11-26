from aiogram.fsm.state import StatesGroup, State


class CardDialog(StatesGroup):
    item = State()
    update = State()
    comment = State()
