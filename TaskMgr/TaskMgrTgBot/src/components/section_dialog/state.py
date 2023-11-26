from aiogram.fsm.state import StatesGroup, State


class SectionDialog(StatesGroup):
    item = State()
    update = State()
