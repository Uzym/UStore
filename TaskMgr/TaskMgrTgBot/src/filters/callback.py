from typing import Optional
from aiogram.filters.callback_data import CallbackData


class FormCallback(CallbackData,prefix="data"):
    obj: str
    tag: str
    cnt: int


class ProjectCallback(CallbackData, prefix="project"):
    action: str
    value: Optional[str] = None


class SectionCallback(CallbackData, prefix="section"):
    action: str
    value: Optional[str] = None


class AddUserCallback(CallbackData, prefix="add_user"):
    obj: str
    user_id: int
    role_id: int
