import operator
from typing import Any

from aiogram import html
from aiogram.types import BotCommand, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Data
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format, Const
from emoji import emojize

from generated import taskmgr
from .state import CardDialog
from src.utils.dialog_builder import DialogBuilder
from src.utils.window_builder import WindowBuilder
from .. import project_dialog
from ..input_dialog.dialog import to_variable, input_variable, start_variable
from ..input_dialog.state import InputDialog
from ..section_dialog.state import SectionDialog
from ..select_object_dialog.state import SelectObjectDialog
from ...lexicon.lexicon import title_lexicon, project_lexicon, description_lexicon, view_lexicon, section_lexicon, \
    card_lexicon
from ...services import ProjectService, CardService
from ...services.odata_service import MyODataService
from ...utils.variable_generator import VariableGenerator


async def on_click_select_section(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=SelectObjectDialog.section_list,
        data={
            to_variable: button_local.widget_id,
            start_variable: True
        }
    )

section_select_button = Button(
    id=str(VariableGenerator(str(taskmgr.Sections.SectionId))),
    text=Const(str(section_lexicon.many)),
    on_click=on_click_select_section
)


async def item_getter(dialog_manager: DialogManager, **kwargs):
    odata_service: MyODataService = MyODataService.instance
    q1 = odata_service.service.query(taskmgr.Cards)
    q1 = q1.filter(
        taskmgr.Cards.CardId == dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))]
    )
    card = q1.first()

    comments = odata_service.service.query(
        taskmgr.Comments
    ).filter(
        taskmgr.Comments.CardId == card.CardId
    ).expand(
        taskmgr.Comments.User
    ).all()

    return {
        str(VariableGenerator(str(taskmgr.Card.Title))): card.Title,
        str(VariableGenerator(str(taskmgr.Card.Description))): card.Description,
        str(VariableGenerator(str(taskmgr.Card.Complete))): card.Complete,
        str(VariableGenerator(str(taskmgr.Card.Comments))): [
            (comment.User.Name, comment.User.TelegramId, comment.Description) for comment in comments
        ],
        str(VariableGenerator(str(taskmgr.Card.Created))): card.Created,
        str(VariableGenerator(str(taskmgr.Card.Due))): card.Due,
        str(VariableGenerator(str(taskmgr.Card.Tags))): card.Tags,
    }

item = WindowBuilder(
    title=str(view_lexicon),
    state=CardDialog.item
).add_widget(
    VariableGenerator(str(taskmgr.Project.Title)).format_title()
).add_widget(
    VariableGenerator(str(taskmgr.Project.Description)).format_description()
).set_getter(
    item_getter
).add_widget(
    section_select_button
)


async def on_click_update_string(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=InputDialog.string,
        data={
            to_variable: button_local.widget_id,
        }
    )

update_title_button = Button(
    id="update_title",
    text=Const(str(title_lexicon.update)),
    on_click=on_click_update_string
)

update_description_button = Button(
    id="update_description",
    text=Const(str(description_lexicon.update)),
    on_click=on_click_update_string
)

update = WindowBuilder(
    title=str(project_lexicon.update),
    state=CardDialog.update
).add_widget(
    VariableGenerator(str(taskmgr.Project.Title)).format_title()
).add_widget(
    VariableGenerator(str(taskmgr.Project.Title)).format_description()
).add_widget(
    update_title_button
).add_widget(
    update_description_button
).set_getter(
    item_getter
)


async def process_result(start_data: Data, result: Any, dialog_manager: DialogManager):
    if result is None:
        return
    project_service = ProjectService.instance
    if result[to_variable] == update_title_button.widget_id:
        await project_service.update_project(
            project_id=int(dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))]),
            title=result[input_variable]
        )
    elif result[to_variable] == update_description_button.widget_id:
        await project_service.update_project(
            project_id=dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Project.ProjectId)))],
            description=result[input_variable]
        )
    elif result[to_variable] == section_select_button.widget_id:
        await dialog_manager.start(
            state=SectionDialog.item,
            data={
                str(VariableGenerator(str(taskmgr.Section.SectionId))): result[input_variable]
            }
        )

dialog_b = DialogBuilder(
    title=str(card_lexicon)
).add_window(
    window_builder=item
).add_window(
    window_builder=update
).set_on_process_result(
    process_result
).set_arbitrary_navigation(
).apply_configuration()

button = dialog_b.get_button()
dialog = dialog_b.get_dialog()
