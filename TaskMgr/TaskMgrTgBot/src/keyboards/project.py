from aiogram.utils.keyboard import InlineKeyboardButton, InlineKeyboardBuilder
from src.filters.callback import ProjectCallback
from aiogram import html
from src.models import domain
from src.services.project_service import parse_link_project
from src.lexicon import LEXICON


def create_projects_keyboard(projects: list):
    builder = InlineKeyboardBuilder()
    for idx, project in enumerate(projects):
        builder.add(InlineKeyboardButton(
            text=f"{idx}: {project.title}",
            callback_data=ProjectCallback(action="get", value=project.project_id).pack()
        ))
        if idx > 20:
            break
    builder.adjust(1, repeat=True)
    return builder.as_markup()


def create_project_action_keyboard(links: list[domain.Link]):
    builder = InlineKeyboardBuilder()
    for idx, link in enumerate(links):
        project_id, action = parse_link_project(link)
        builder.add(InlineKeyboardButton(
            text=LEXICON[action + "_project"],
            callback_data=ProjectCallback(action=action, value=project_id).pack()
        ))
        if idx > 20:
            break
    builder.adjust(1, repeat=True)
    return builder.as_markup()

