from datetime import date, timedelta

from aiogram.types import CallbackQuery, BotCommand
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Format

from generated.taskmgr import Cards
from src.components.input_dialog.dialog import to_variable
from src.components.input_dialog.state import InputDialog
from src.components.select_object_dialog.builders.card_list import on_click_item_card
from src.components.select_object_dialog.filter import CardFilter, get_filter_buttons
from src.components.select_object_dialog.state import SelectObjectDialog
from src.lexicon.lexicon import down_lexicon, back_lexicon, next_lexicon, card_lexicon, calendar_lexicon
from src.utils.variable_generator import VariableGenerator
from src.utils.window_builder import WindowBuilder


async def cards_getter(dialog_manager: DialogManager, **kwargs):
    return await CardFilter(dialog_manager).calendar_view()


async def on_click_current_date_update(callback: CallbackQuery, button_local: Button, manager: DialogManager):
    await manager.start(
        state=InputDialog.date,
        data={
            to_variable: button_local.widget_id
        }
    )

update_current_date_button = Button(
    id="update_current_date_button",
    text=Format(text=str(down_lexicon.prefix) + "{current_date}" + str(down_lexicon.suffix)),
    on_click=on_click_current_date_update
)


async def on_click_current_date_prev(callback: CallbackQuery, button: Button, manager: DialogManager):
    current_date: date = manager.start_data[str(VariableGenerator("current_date"))] - timedelta(days=1)
    manager.start_data[
        str(VariableGenerator("current_date"))
    ] = current_date

update_current_date_before_button = Button(
    id="update_current_date_before_button",
    text=Format(text=str(back_lexicon.prefix) + "Пропущено"),
    on_click=on_click_current_date_prev
)


async def on_click_current_date_next(callback: CallbackQuery, button: Button, manager: DialogManager):
    current_date: date = manager.start_data[str(VariableGenerator("current_date"))] + timedelta(days=1)
    manager.start_data[
        str(VariableGenerator("current_date"))
    ] = current_date

update_current_date_future_button = Button(
    id="update_current_date_future_button",
    text=Format(text="Будущее" + str(next_lexicon.suffix)),
    on_click=on_click_current_date_next
)

card_calendar = WindowBuilder(
    title=str(card_lexicon.many),
    state=SelectObjectDialog.card_calendar
).set_command(
    command=BotCommand(command="calendar", description="Ваши задачи представленные в виде простого календаря")
).add_widget(
    get_filter_buttons()
).add_widget(
    update_current_date_before_button
).add_simple_select(
    on_click_item_card, str(VariableGenerator(str(Cards) + "_before")), 10, 1
).add_widget(
    update_current_date_button
).add_simple_select(
    on_click_item_card, str(VariableGenerator(str(Cards) + "_now")), 10, 1
).add_widget(
    update_current_date_future_button
).add_simple_select(
    on_click_item_card, str(VariableGenerator(str(Cards) + "_future")), 10, 1
).set_getter(
    cards_getter
).set_navigation(
    [str(calendar_lexicon)]
)
