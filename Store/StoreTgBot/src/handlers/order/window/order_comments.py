import operator
import logging

from typing import Any
from aiogram import html
from aiogram.types import CallbackQuery, Message
from datetime import date

from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Calendar
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput

from src.lexicon import LEXICON
from src.services import OrderService, ProductService
from src.states.states import Order

order_service = OrderService()
product_service = ProductService()
logger = logging.getLogger()


