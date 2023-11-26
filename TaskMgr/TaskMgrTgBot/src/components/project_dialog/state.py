from aiogram.fsm.state import StatesGroup, State


class ProjectDialog(StatesGroup):
    item = State()
    update = State()
