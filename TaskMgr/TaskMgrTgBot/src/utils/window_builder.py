import operator
import uuid
from typing import Optional

from aiogram.filters import Command
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery, BotCommand, Message
from aiogram_dialog import Window, DialogManager, StartMode
from aiogram_dialog.api.internal import Widget
from aiogram_dialog.widgets.kbd import Button, Group, Cancel, ScrollingGroup, Select
from aiogram_dialog.widgets.text import Const, Format
from aiogram import html, Router
from emoji import emojize

from src.lexicon.lexicon import cancel_lexicon


class WindowBuilder:
    instances = []

    def __init__(self, title: str, state: State):
        WindowBuilder.instances.append(self)
        self.title: str = title
        self.state: State = state
        self.getter = None
        self.navigation = []
        self.navigation_buttons: Group = Group()
        self.widgets: list[Widget] = []
        self.command: Optional[BotCommand] = None
        self.done_key = None

    def set_command(self, command: BotCommand):
        self.command = command
        return self

    def set_getter(self, getter):
        self.getter = getter
        return self

    def set_done_key(self, done_key: str):
        self.done_key = done_key
        return self

    def set_navigation_buttons(self, navigation_buttons: Group):
        self.navigation_buttons = navigation_buttons
        return self

    def add_widget(self, widget: Widget):
        self.widgets.append(widget)
        return self

    def add_simple_select(self, on_click_handler, items_name: str, height: int, width: int):
        self.widgets.append(ScrollingGroup(
            Select(
                text=Format("{item[1]}"),
                id="items_selector_s",
                items=items_name,
                item_id_getter=operator.itemgetter(0),
                on_click=on_click_handler
            ),
            height=height,
            width=width,
            id="items_selector"
        ))
        return self

    def set_navigation(self, parent_navigation: list[str]):
        if len(self.navigation) == 0:
            self.navigation = parent_navigation + [self.title] + self.navigation
        else:
            self.navigation = parent_navigation + [self.title] + self.navigation[:len(self.navigation) - 1]
        return self

    def get_window(self) -> Window:
        return Window(
            Const(html.bold(self.get_title())),
            *self.widgets,
            self.navigation_buttons,
            Cancel(Const(str(cancel_lexicon))),
            state=self.state,
            getter=self.getter
        )

    def get_title(self) -> str:
        return emojize(" / ").join(self.navigation)

    def get_button(self) -> Button:
        return Button(
            text=Const(self.title),
            id=str(self.state.state.title()).replace(":", "_"),
            on_click=on_click_navigation_button
        )


async def on_click_navigation_button(callback: CallbackQuery, button: Button, manager: DialogManager):
    state_title = button.widget_id.replace("_", ":")
    state: State = None
    for builder in WindowBuilder.instances:
        if builder.state is None:
            continue
        if builder.state.state.title() == state_title:
            state = builder.state
    try:
        await manager.switch_to(state=state)
    except:
        return
