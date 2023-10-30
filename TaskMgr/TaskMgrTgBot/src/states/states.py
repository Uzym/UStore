from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

class DefualtForm(StatesGroup):
    user_input = State()

class AddUserForm(StatesGroup):
    project_add_user = State()

class AddSectionForm(StatesGroup):
    project_add_section = State()

class UpdateProjectForm(StatesGroup):
    project_update_title = State()
    project_update_description = State()
