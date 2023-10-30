from aiogram import Router
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandObject
from magic_filter import F
from aiogram.fsm.context import FSMContext

from src.keyboards.keyboards import create_get_objects_keyboard
from src.keyboards.project import create_projects_keyboard, create_project_action_keyboard
from src.keyboards.section import create_section_keyboard
from src.keyboards.user import create_users_keyboard, create_select_user_role_keyboard
from src.lexicon import LEXICON
from src.services import ProjectService, UserService, RoleService
from src.filters.callback import ProjectCallback, AddUserCallback, SectionCallback
from src.states.states import AddUserForm, AddSectionForm, UpdateProjectForm

router: Router = Router()


@router.message(Command(commands=["projects"]))
async def get_projects(message: Message, project_service: ProjectService):
    try:
        projects = await project_service.projects(telegram_id=str(message.from_user.id))
        keyboard = create_projects_keyboard(projects)
        await message.answer(text=LEXICON["projects"],
                             reply_markup=keyboard)
    except:
        await message.answer(text=LEXICON["not_found"])


@router.callback_query(ProjectCallback.filter(F.action == "get"))
async def get_project(
        callback: CallbackQuery,
        callback_data: ProjectCallback,
        project_service: ProjectService
):
    await callback.answer(text=LEXICON["loading"])
    try:
        response = await project_service.get_project(
            project_id=int(callback_data.value),
            telegram_id=str(callback.from_user.id)
        )
        await callback.answer(text=str(response.project))
        keyboard = create_project_action_keyboard(response.links)
        await callback.message.answer(
            text=str(response.project),
            reply_markup=keyboard
        )

    except:
        await callback.answer(text=LEXICON["not_found"])


@router.callback_query(ProjectCallback.filter(F.action == "update"))
async def start_update(
        callback: CallbackQuery,
        callback_data: ProjectCallback,
        state: FSMContext
):
    await callback.answer(text=LEXICON["loading"])
    try:
        await state.clear()
        await state.set_state(UpdateProjectForm.project_update_title)
        await state.set_data({})
        await state.set_data({"project_id": callback_data.value})
        await callback.message.answer(text=LEXICON["start_update_project"])
    except:
        await callback.answer(text=LEXICON["not_found"])


@router.message(UpdateProjectForm.project_update_title)
async def title_update(
        message: Message,
        state: FSMContext,
):
    try:
        data = await state.get_data()
        data["title"] = message.text
        await state.set_data(data)
        await state.set_state(UpdateProjectForm.project_update_description)
    except:
        await message.answer(text=LEXICON["not_found"])


@router.message(UpdateProjectForm.project_update_description)
async def description_update(
        message: Message,
        state: FSMContext,
        project_service: ProjectService
):
    try:
        data = await state.get_data()
        project = await project_service.update_project(data["project_id"], data["title"], message.text)
        await message.answer(text=LEXICON["end_update_project"])
        await message.answer(text=str(project))
        await state.clear()
    except:
        await message.answer(text=LEXICON["not_found"])


@router.callback_query(ProjectCallback.filter(F.action == "add_section"))
async def start_add_section(
        callback: CallbackQuery,
        callback_data: ProjectCallback,
        state: FSMContext
):
    await callback.answer(text=LEXICON["loading"])
    try:
        await state.clear()
        await state.set_state(AddSectionForm.project_add_section)
        await state.set_data({})
        await state.set_data({"project_id": callback_data.value})
        await callback.message.answer(text=LEXICON["start_add_section"])
    except:
        await callback.answer(text=LEXICON["not_found"])


@router.message(AddSectionForm.project_add_section)
async def end_add_section(
        message: Message,
        state: FSMContext,
        project_service: ProjectService
):
    try:
        project_id = (await state.get_data())["project_id"]
        section = await project_service.add_section_to_project(project_id, message.text)
        await message.answer(text=LEXICON["end_add_section"])
        await message.answer(text=str(section))
        await state.clear()
    except:
        await message.answer(text=LEXICON["not_found"])


@router.callback_query(ProjectCallback.filter(F.action == "get_section"))
async def get_sections(
        callback: CallbackQuery,
        callback_data: ProjectCallback,
        project_service: ProjectService,
):
    await callback.answer(text=LEXICON["loading"])
    try:
        sections = await project_service.get_sections(int(callback_data.value))
        markup = create_get_objects_keyboard(
            callback_factory=SectionCallback,
            data=[
                (section.title, section.section_id) for section in sections
            ],
        )
        await callback.message.answer(
            text=LEXICON["get_section_project"],
            reply_markup=markup
        )
    except:
        await callback.answer(text=LEXICON["not_found"])


@router.callback_query(ProjectCallback.filter(F.action == "add_user"))
async def start_add_user(
        callback: CallbackQuery,
        callback_data: ProjectCallback,
        state: FSMContext,
):
    await callback.answer(text=LEXICON["loading"])
    try:
        await state.clear()
        await state.set_state(AddUserForm.project_add_user)
        await state.set_data({})
        await state.set_data({"project_id": callback_data.value})
        await callback.message.answer(text=LEXICON["start_add_user"])
    except:
        await callback.answer(text=LEXICON["not_found"])


@router.message(AddUserForm.project_add_user)
async def select_add_user(
        message: Message,
        state: FSMContext,
        user_service: UserService,
        role_service: RoleService
):
    try:
        users = await user_service.users(name=message.text)
        roles = await role_service.roles(table="project")
        keyboard = create_select_user_role_keyboard("project", users, roles)
        await message.answer(text=LEXICON["add_user_message"], reply_markup=keyboard)
    except:
        await message.answer(text=LEXICON["not_found"])


@router.callback_query(AddUserCallback.filter(F.obj == "project"))
async def end_add_user(
        callback: CallbackQuery,
        callback_data: AddUserCallback,
        project_service: ProjectService,
        state: FSMContext,
):
    await callback.answer(text=LEXICON["loading"])
    try:
        project_id = (await state.get_data())["project_id"]
        await project_service.add_user_to_project(
            project_id=project_id,
            user_id=callback_data.user_id,
            role_id=callback_data.role_id
        )
        await callback.message.answer(
            text=LEXICON["end_add_user"]
        )
        await state.clear()
    except:
        await callback.answer(text=LEXICON["not_found"])


@router.callback_query(ProjectCallback.filter(F.action == "get_user"))
async def get_users(
        callback: CallbackQuery,
        callback_data: ProjectCallback,
        project_service: ProjectService,
        user_service: UserService,
        role_service: RoleService
):
    await callback.answer(text=LEXICON["loading"])
    try:
        user_roles = await project_service.get_users(int(callback_data.value))
        users = []
        roles = []
        for user_role in user_roles:
            user = await user_service.get_user(user_role.user_id)
            role = await role_service.get_role(user_role.role_id)
            users.append(user)
            roles.append(role.title)
        keyboard = create_users_keyboard(users, roles)
        await callback.message.answer(
            text=LEXICON["get_user_project"],
            reply_markup=keyboard
        )
    except:
        await callback.answer(text=LEXICON["not_found"])


@router.message(Command(commands=["new_project"]))
async def new_project(
        message: Message,
        command: CommandObject,
        project_service: ProjectService,
        role_service: RoleService,
        user_service: UserService):
    try:
        if len(command.args) != 0:
            await message.answer(text=LEXICON["bad_input"])
            return

        project = await project_service.create_project(title=command.args, description=LEXICON["defualt_description_project"])
        user = await user_service.users(telegram_id=str(message.from_user.id))
        role = await role_service.roles(
            description="telegram creator project role"
        )
        if len(role) == 0:
            await message.answer(text=LEXICON["not_found"])
            return
        await project_service.add_user_to_project(
            project_id=project.project_id,
            role_id=role[0].role_id,
            user_id=user[0].user_id
        )
        await message.answer(text=LEXICON["new_project_good"])
        await message.answer(text=str(project))
    except:
        await message.answer(text=LEXICON["not_found"])
