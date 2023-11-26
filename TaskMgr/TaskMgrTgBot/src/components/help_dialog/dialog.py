from aiogram import Router
from aiogram.types import BotCommand
from aiogram_dialog import Dialog
from emoji import emojize

from src.components.help_dialog.state import HelpDialog
from src.lexicon.lexicon import menu_lexicon
from src.utils.dialog_builder import DialogBuilder
from src.utils.window_builder import WindowBuilder


menu = WindowBuilder(
    title=str(menu_lexicon),
    state=HelpDialog.menu
).set_command(
    command=BotCommand(command="help", description="справка пользователя по боту")
)

faq = WindowBuilder(
    title="FAQ",
    state=HelpDialog.faq
)

commands = WindowBuilder(
    title="Команды",
    state=HelpDialog.commands
)

guide = WindowBuilder(
    title="Руководство",
    state=HelpDialog.guide
)

dialog_b = DialogBuilder(
    title=emojize(":red_question_mark:Помощь")
).add_window(
    window_builder=menu
).add_window(
    window_builder=faq
).add_window(
    window_builder=commands
).add_window(
    window_builder=guide
).set_arbitrary_navigation(

).apply_configuration()

button = dialog_b.get_button(HelpDialog.menu)
dialog = dialog_b.get_dialog()
