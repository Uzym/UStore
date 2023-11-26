from aiogram.fsm.state import StatesGroup, State


class HelpDialog(StatesGroup):
    menu = State()
    commands = State()
    guide = State()
    faq = State()
