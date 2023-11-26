import uuid

from aiogram import html
from aiogram_dialog.widgets.text import Format


class VariableGenerator:
    def __init__(self, var_name: str):
        self.var_name = var_name.replace(
            "(", "_"
        ).replace(
            ")", ""
        ).replace(
            "<", ""
        ).replace(
            ">", ""
        )

    def format_variable(self):
        return f"{{{self.var_name}}}"

    def __str__(self):
        return self.var_name

    def __call__(self, *args, **kwargs):
        return self.__str__()

    def format_title(self):
        return Format(html.bold(self.format_variable()))

    def format_description(self):
        return Format(html.italic(self.format_variable()))
