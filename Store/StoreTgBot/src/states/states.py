from aiogram.fsm.state import State, StatesGroup


class Main(StatesGroup):
    main = State()
    get_me = State()
    help = State()


class Firm(StatesGroup):
    firms_search = State()
    firms_search_title_filter = State()
    firms_search_description_filter = State()
    firms_search_discount_filter = State()
    firm_create = State()
    firm_create_title_param = State()
    firm_create_description_param = State()
    firm_create_discount_param = State()
    firms = State()
    firm = State()