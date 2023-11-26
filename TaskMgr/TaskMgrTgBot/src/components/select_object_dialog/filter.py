from datetime import datetime
from typing import Type

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ChatEvent
from aiogram_dialog.widgets.kbd import Button, Checkbox, ManagedCheckbox, Group, Row
from aiogram_dialog.widgets.text import Format, Const
from odata.query import Query

from generated import taskmgr
from generated.taskmgr import Cards
from src.components.input_dialog.dialog import to_variable, start_variable
from src.components.select_object_dialog.state import SelectObjectDialog
from src.lexicon.lexicon import section_lexicon, project_lexicon, include_lexicon, un_include_lexicon
from src.services import UserService
from src.services.odata_service import MyODataService
from src.utils.variable_generator import VariableGenerator


def prepare_data_to_button(items: list):
    return [(str(item["CardId"]), str(item["Title"])) for item in items]


async def on_click_project_filter(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(
        state=SelectObjectDialog.project_list,
        data={
            to_variable: button.widget_id,
            start_variable: False
        }
    )

select_project_button = Button(
    text=Format(str(project_lexicon)),
    id="select_project_id_filter",
    on_click=on_click_project_filter
)


async def on_click_section_filter(callback: CallbackQuery, button: Button, manager: DialogManager):
    await manager.start(
        state=SelectObjectDialog.section_list,
        data={
            to_variable: button.widget_id,
            start_variable: False,
            str(VariableGenerator(str(taskmgr.Project.ProjectId))): manager.start_data[
                str(VariableGenerator(str(taskmgr.Project.ProjectId)))
            ]
        }
    )

select_section_button = Button(
    text=Format(str(section_lexicon)),
    id="select_section_id_filter",
    on_click=on_click_section_filter,
    when=F["start_data"][str(VariableGenerator(str(taskmgr.Project.ProjectId)))].is_not(None)
)


def get_filter_buttons():
    return Group(
        Row(
            select_project_button,
            select_section_button,
            id="filter_group_card_selects"
        ),
        Group(
            Checkbox(
                Const(str(include_lexicon) + " выполненные"),
                Const(str(un_include_lexicon) + " выполненные"),
                id="check_complete_cards_filter",
                default=False,
                on_click=check_complete_changed
            ),
            # Checkbox(
            #     Const(str(include_lexicon) + " мои карточки"),
            #     Const(str(un_include_lexicon) + " мои карточки"),
            #     id="check_user_cards_filter",
            #     default=False,
            #     on_click=check_user_changed
            # ),
            id="filter_group_card_checkbox",
            width=1
        ),
        id="filter_group_card"
    )


class CardFilter:
    def __prepare_start_data(self):
        if not (str(VariableGenerator("view")) in self.dialog_manager.start_data.keys()):
            self.dialog_manager.start_data[str(VariableGenerator("view"))] = str(VariableGenerator("calendar"))
        if not (str(VariableGenerator("current_date")) in self.dialog_manager.start_data.keys()):
            self.dialog_manager.start_data[str(VariableGenerator("current_date"))] = datetime.now().date()

    def __init__(self, dialog_manager: DialogManager):
        self.dialog_manager = dialog_manager
        self.__prepare_start_data()
        self.telegram_id = str(dialog_manager.event.from_user.id)
        self.q: Query[Type[Cards]] = MyODataService.instance.service.query(Cards)

        self.section_id = dialog_manager.start_data.get(str(VariableGenerator(str(taskmgr.Section.SectionId))))
        self.project_id = dialog_manager.start_data.get(str(VariableGenerator(str(taskmgr.Project.ProjectId))))
        self.complete = dialog_manager.start_data.get(str(VariableGenerator(str(taskmgr.Card.Complete))))
        self.user = dialog_manager.start_data.get(str(VariableGenerator(str(taskmgr.Card.UserCards))))
        self.current_date = dialog_manager.start_data[str(VariableGenerator("current_date"))]

    async def filter_by_user(self):
        user_service: UserService = UserService.instance
        user = (await user_service.users(telegram_id=self.telegram_id))[0]
        self.q = self.q.expand(Cards.UserCards)
        self.q = self.q.filter(any(user.user_id == item.UserId for item in Cards.UserCards))

    def filter_by_section(self):
        self.q = self.q.filter(Cards.SectionId == self.section_id)

    def filter_by_project(self):
        self.q = self.q.expand(Cards.Section)
        self.q = self.q.filter(Cards.Section.ProjectId == self.project_id)

    def filter_complete(self):
        if self.complete == "un include":
            self.q = self.q.filter(Cards.Complete != None)

    async def calendar_view(self):
        await self.prepare_filter()
        self.q = self.q.select(Cards.CardId, Cards.Title, Cards.Due)

        items_before = self.q.filter(Cards.Due < self.current_date).all()
        items_now = self.q.filter(Cards.Due == self.current_date).all()
        items_future = self.q.filter(Cards.Due > self.current_date).all()

        print(items_future, items_now, items_before)

        return {
            str(VariableGenerator(str(Cards) + "_before")): prepare_data_to_button(items_before),
            str(VariableGenerator(str(Cards) + "_now")): prepare_data_to_button(items_now),
            str(VariableGenerator(str(Cards) + "_future")): prepare_data_to_button(items_future),
            "current_date": self.current_date
        }

    async def list_view(self):
        await self.prepare_filter()
        self.q = self.q.select(Cards.CardId, Cards.Title)
        items = self.q.all()
        return {
            str(VariableGenerator(str(Cards))): prepare_data_to_button(items)
        }

    async def prepare_filter(self):
        if self.section_id is not None:
            self.filter_by_section()
        if self.project_id is not None:
            self.filter_by_project()
        if self.complete is not None:
            self.filter_complete()
        if self.user is not None:
            await self.filter_by_user()


async def check_complete_changed(event: ChatEvent, checkbox: ManagedCheckbox, manager: DialogManager):
    if checkbox.is_checked():
        manager.start_data[str(VariableGenerator(str(taskmgr.Card.Complete)))] = "include"
    else:
        manager.start_data[str(VariableGenerator(str(taskmgr.Card.Complete)))] = "un include"


async def check_user_changed(event: ChatEvent, checkbox: ManagedCheckbox, manager: DialogManager):
    if checkbox.is_checked():
        manager.start_data[str(VariableGenerator(str(taskmgr.Card.UserCards)))] = True
    else:
        manager.start_data[str(VariableGenerator(str(taskmgr.Card.UserCards)))] = None
