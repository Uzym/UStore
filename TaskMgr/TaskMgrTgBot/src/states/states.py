from aiogram.fsm.context import FSMContext
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
    card = State()
    update_title = State()
    update_description = State()
    update_tags = State()
    update_due = State()


class NewProject(StatesGroup):
    new_project_title = State()
    new_project_description = State()
    new_project_ok = State()

class DefualtForm(StatesGroup):
    user_input = State()

class AddUserForm(StatesGroup):
    project_add_user = State()

class AddSectionForm(StatesGroup):
    project_add_section = State()

class UpdateProjectForm(StatesGroup):
    project_update_title = State()
    project_update_description = State()
