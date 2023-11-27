from typing import Any

from aiogram import html, F
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, Data
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.text import Format, Const, List

from generated import taskmgr
from .state import CardDialog
from src.utils.dialog_builder import DialogBuilder
from src.utils.window_builder import WindowBuilder
from ..input_dialog.dialog import to_variable, input_variable, start_variable
from ..input_dialog.state import InputDialog
from ..select_object_dialog.state import SelectObjectDialog
from ...lexicon.lexicon import (title_lexicon, description_lexicon, view_lexicon, card_lexicon, comment_lexicon,
                                created_lexicon, complete_lexicon, due_lexicon, tags_lexicon, due_prop_lexicon,
                                section_lexicon, un_complete_lexicon)
from ...services import CardService
from ...services.odata_service import MyODataService
from ...utils.variable_generator import VariableGenerator


async def item_getter(dialog_manager: DialogManager, **kwargs):
    odata_service: MyODataService = MyODataService.instance
    q1 = odata_service.service.query(taskmgr.Cards)
    q1 = q1.filter(
        taskmgr.Cards.CardId == dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))]
    )
    card = q1.first()

    return {
        str(VariableGenerator(str(taskmgr.Card.Title))):
            card.Title if card.Title is not None else "",
        str(VariableGenerator(str(taskmgr.Card.Description))):
            card.Description if card.Description is not None else "",
        str(VariableGenerator(str(taskmgr.Card.Complete))):
            card.Complete.strftime("%d-%m-%Y %H:%M") if card.Complete is not None else "",
        str(VariableGenerator(str(taskmgr.Card.Created))):
            card.Created.strftime("%d-%m-%Y %H:%M") if card.Created is not None else "",
        str(VariableGenerator(str(taskmgr.Card.Due))):
            card.Due.strftime("%d-%m-%Y %H:%M") if card.Due is not None else "",
        str(VariableGenerator(str(taskmgr.Card.Tags))):
            "#" + " #".join(card.Tags) if len(card.Tags) != 0 else "",
    }


async def on_click_select_section(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=SelectObjectDialog.section_list,
        data={
            to_variable: button_local.widget_id,
            start_variable: False
        }
    )

section_select_button = Button(
    id=str(VariableGenerator(str(taskmgr.Sections.SectionId))),
    text=Const(str(section_lexicon.update)),
    on_click=on_click_select_section
)


async def on_click_complete_card(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    card_service: CardService = CardService.instance
    await card_service.complete_card(manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))])

card_complete_button = Button(
    id=str(VariableGenerator(str(taskmgr.Card.Complete))),
    text=Const(str(complete_lexicon)),
    on_click=on_click_complete_card
)


async def on_click_un_complete_card(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    card_service: CardService = CardService.instance
    await card_service.uncomplete_card(manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))])

card_un_complete_button = Button(
    id=str(VariableGenerator(str(taskmgr.Card.Complete))),
    text=Const(str(un_complete_lexicon)),
    on_click=on_click_un_complete_card
)

item = WindowBuilder(
    title=str(view_lexicon),
    state=CardDialog.item
).add_widget(
    VariableGenerator(str(taskmgr.Card.Title)).format_title()
).add_widget(
    VariableGenerator(str(taskmgr.Card.Description)).format_description()
).add_widget(
    VariableGenerator(str(taskmgr.Card.Tags)).format_item()
).add_widget(
    VariableGenerator(str(taskmgr.Card.Created)).format_item(created_lexicon.prefix)
).add_widget(
    VariableGenerator(str(taskmgr.Card.Complete)).format_item(complete_lexicon.prefix)
).add_widget(
    VariableGenerator(str(taskmgr.Card.Due)).format_item(due_lexicon.prefix)
).add_widget(
    section_select_button
).add_widget(
    Row(card_complete_button, card_un_complete_button, id="row_complete_or_un_complete")
).set_getter(
    item_getter
)


async def on_click_update_string(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=InputDialog.string,
        data={
            to_variable: button_local.widget_id,
        }
    )


async def on_click_update_date(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=InputDialog.date,
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

update_tags_button = Button(
    id="update_tags",
    text=Const(str(tags_lexicon.update)),
    on_click=on_click_update_string
)

update_due_button = Button(
    id="update_due",
    text=Const(str(due_prop_lexicon.update)),
    on_click=on_click_update_date
)

update = WindowBuilder(
    title=str(card_lexicon.update),
    state=CardDialog.update
).add_widget(
    VariableGenerator(str(taskmgr.Card.Title)).format_title()
).add_widget(
    VariableGenerator(str(taskmgr.Card.Description)).format_description()
).add_widget(
    VariableGenerator(str(taskmgr.Card.Tags)).format_item()
).add_widget(
    VariableGenerator(str(taskmgr.Card.Created)).format_item(created_lexicon.prefix)
).add_widget(
    VariableGenerator(str(taskmgr.Card.Complete)).format_item(complete_lexicon.prefix)
).add_widget(
    VariableGenerator(str(taskmgr.Card.Due)).format_item(due_lexicon.prefix)
).add_widget(
    update_title_button
).add_widget(
    update_description_button
).add_widget(
    update_tags_button
).add_widget(
    update_due_button
).set_getter(
    item_getter
)


async def comment_getter(dialog_manager: DialogManager, **kwargs):
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
        str(VariableGenerator(str(taskmgr.Card.Comments))): [
            f"{html.link(value=item_comment.User.Name, link=f'tg://user?id={item_comment.User.TelegramId}')}: "
            f"{item_comment.Description}"
            for item_comment in comments
        ]
    }


async def add_comment(message: Message, message_input: MessageInput, manager: DialogManager):
    card_service: CardService = CardService.instance
    await card_service.create_comment(
        telegram_id=str(manager.event.from_user.id),
        description=message.text,
        card_id=manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))]
    )

comment = WindowBuilder(
    title=str(comment_lexicon.many),
    state=CardDialog.comment
).add_widget(
    List(
        Format("{item}"),
        items=str(VariableGenerator(str(taskmgr.Card.Comments)))
    )
).add_widget(
    MessageInput(
        filter=F.text,
        func=add_comment
    )
).set_getter(
    comment_getter
)


async def process_result(start_data: Data, result: Any, dialog_manager: DialogManager):
    if result is None:
        return
    card_service: CardService = CardService.instance
    if result[to_variable] == update_title_button.widget_id:
        await card_service.update_card(
            card_id=int(dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))]),
            title=result[input_variable]
        )
    elif result[to_variable] == update_description_button.widget_id:
        await card_service.update_card(
            card_id=dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))],
            description=result[input_variable]
        )
    elif result[to_variable] == update_tags_button.widget_id:
        data = result[input_variable].split(" #")
        data = [item_data.replace("#", "").replace(" ", "_") for item_data in data]
        await card_service.update_card(
            card_id=dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))],
            tags=data
        )
    elif result[to_variable] == update_due_button.widget_id:
        await card_service.update_card(
            card_id=dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))],
            due=str(result[input_variable])
        )
    elif result[to_variable] == section_select_button.widget_id:
        await card_service.update_card(
            card_id=dialog_manager.start_data[str(VariableGenerator(str(taskmgr.Card.CardId)))],
            section_id=int(result[input_variable])
        )

dialog_b = DialogBuilder(
    title=str(card_lexicon)
).add_window(
    window_builder=item
).add_window(
    window_builder=update
).add_window(
    window_builder=comment
).set_on_process_result(
    process_result
).set_arbitrary_navigation(
).apply_configuration()

button = dialog_b.get_button()
dialog = dialog_b.get_dialog()
