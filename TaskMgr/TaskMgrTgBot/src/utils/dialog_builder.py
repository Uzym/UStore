import uuid

from aiogram import Router
from aiogram.fsm.state import State
from aiogram.types import BotCommand, CallbackQuery
from aiogram_dialog import Window, Dialog, DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Back, Button, Group, Start, Next
from aiogram_dialog.widgets.text import Const

from src.lexicon.lexicon import back_lexicon, next_lexicon
from src.utils.window_builder import WindowBuilder


class DialogBuilder:

    def __init__(self, title: str):
        self.title: str = title
        self.windows: list[WindowBuilder] = []
        self.on_process_result = None
        self.getter = None

    def add_window(self, window_builder: WindowBuilder):
        self.windows.append(window_builder)
        return self

    def get_commands(self) -> list[tuple[BotCommand, State]]:
        return [(window.command, window.state) for window in self.windows]

    def set_arbitrary_navigation(self):
        navigation_buttons: list[Button] = []

        for window_builder in self.windows:
            navigation_buttons.append(window_builder.get_button())

        for idx, window_builder in enumerate(self.windows):
            navigation_group = []
            for jdx, button in enumerate(navigation_buttons):
                if idx == jdx:
                    continue
                navigation_group.append(button)
            window_builder.set_navigation_buttons(Group(
                *navigation_group,
                id="s_navigation_buttons",
                width=3
            ))

        return self

    def set_getter(self, getter):
        self.getter = getter
        return self

    def set_on_process_result(self, on_process_result):
        self.on_process_result = on_process_result
        return self

    def set_sequential_navigation(self):
        for idx, window_builder in enumerate(self.windows):
            navigation_group = []
            if idx != 0:
                navigation_group.append(Back(Const(str(back_lexicon))))
            if idx != len(self.windows) - 1:
                navigation_group.append(Next(Const(str(next_lexicon))))
            window_builder.set_navigation_buttons(Group(
                *navigation_group,
                id="s_navigation_buttons",
                width=2
            ))

        return self

    def set_return_navigation(self):
        navigation_button: Button = self.windows[0].get_button()

        flag = False
        for idx, window_builder in enumerate(self.windows):
            if flag:
                window_builder.set_navigation_buttons(Group(
                    navigation_button,
                    id="s_navigation_buttons",
                    width=3
                ))
            flag = True

        return self

    def apply_configuration(self):
        for idx, window_builder in enumerate(self.windows):
            window_builder.set_navigation([self.title])

        return self

    def get_dialog(self) -> Dialog:
        windows = []
        for idx, window_builder in enumerate(self.windows):
            windows.append(window_builder.get_window())

        return Dialog(
            *windows,
            on_process_result=self.on_process_result,
            getter=self.getter
        )

    def get_button(self, state: State = None) -> Button:
        for window_builder in self.windows:
            if window_builder.state == state:
                print(window_builder.title)
                return Start(
                    text=Const(window_builder.get_title()),
                    id="start_" + str(window_builder.state.state.title()).replace(":", "_"),
                    state=window_builder.state
                )

        return Start(
            text=Const(self.title),
            id="start_" + str(self.windows[0].state.state.title()).replace(":", "_"),
            state=self.windows[0].state
        )
