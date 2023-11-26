from aiogram.fsm.state import StatesGroup, State


class SelectObjectDialog(StatesGroup):
    project_list = State()
    section_list = State()
    card_list = State()
    card_calendar = State()
