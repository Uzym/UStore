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
    firm_update = State()
    firm_update_title = State()
    firm_update_description = State()
    firm_update_discount = State()
    firm_wait_photo = State()
    firm_delete_photo = State()
    firms = State()
    firm = State()


class Category(StatesGroup):
    categories_search = State()
    categories_search_title_filter = State()
    categories_search_description_filter = State()
    categories_search_discount_filter = State()
    category_create = State()
    category_create_title_param = State()
    category_create_description_param = State()
    category_create_discount_param = State()
    category_update = State()
    category_update_title = State()
    category_update_description = State()
    category_update_discount = State()
    category_wait_photo = State()
    category_delete_photo = State()
    categories = State()
    category = State()
    