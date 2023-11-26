from aiogram.fsm.state import State, StatesGroup


class Main(StatesGroup):
    main = State()
    get_me = State()
    help = State()


class Project(StatesGroup):
    projects = State()
    project = State()
    project_update = State()
    project_update_title = State()
    project_update_description = State()
    project_get_user = State()
    project_add_user = State()


class Section(StatesGroup):
    section = State()
    update = State()
    update_title = State()


class Card(StatesGroup):
    cards = State()
    card = State()
    update_title = State()
    update_description = State()
    update_tags = State()
    update_due = State()
    update_section = State()
    users = State()
    add_user = State()
    comments = State()
    add_comment = State()
