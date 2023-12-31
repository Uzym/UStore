from aiogram.fsm.state import State, StatesGroup


class Main(StatesGroup):
    main = State()
    get_me = State()
    help = State()
    update_address = State()
    update_telephone = State()
    update_email = State()


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


class Series(StatesGroup):
    series_search = State()
    series_search_firms_list = State()
    series_search_categories_list = State()
    series_search_title_filter = State()
    series_search_description_filter = State()
    series_search_discount_filter = State()
    series_create = State()
    series_create_firms_list = State()
    series_create_title_param = State()
    series_create_description_param = State()
    series_create_discount_param = State()
    series_update = State()
    series_update_title = State()
    series_update_description = State()
    series_update_discount = State()
    series_update_firms_list = State()
    series_wait_photo = State()
    series_delete_photo = State()
    series_list = State()
    series = State()


class Product(StatesGroup):
    products_search = State()
    products_search_firms_list = State()
    products_search_categories_list = State()
    products_search_series_list = State()
    products_search_title_filter = State()
    products_search_description_filter = State()
    products_search_discount_filter = State()
    products_search_cost_filter = State()
    products_search_delivery_time_filter = State()
    product_create = State()
    product_create_categories_list = State()
    product_create_series_list = State()
    product_create_title_param = State()
    product_create_description_param = State()
    product_create_discount_param = State()
    product_create_cost_param = State()
    product_create_delivery_time_param = State()
    product_update = State()
    product_update_title = State()
    product_update_description = State()
    product_update_discount = State()
    product_update_cost = State()
    product_update_delivery_time = State()
    product_update_categories_list = State()
    product_update_series_list = State()
    product_wait_photo = State()
    product_delete_photo = State()
    products = State()
    product = State()


class User(StatesGroup):
    users_search = State()
    users_search_tg_id_filter = State()
    user_update_admin = State()
    users = State()
    user = State()


class Order(StatesGroup):
    orders_history = State()
    order = State()
    order_card = State()
    order_comments = State()
    order_comment = State()
    add_comment = State()
