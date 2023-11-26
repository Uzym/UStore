from aiogram.fsm.state import StatesGroup, State


class InputDialog(StatesGroup):
    string = State()
    date = State()
    select_item = State()
