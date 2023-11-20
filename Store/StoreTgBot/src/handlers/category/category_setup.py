from aiogram import Router
from aiogram.filters import Command, and_f
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Dialog
from src.filters import IsAdmin
from src.lexicon.lexicon import FIRMS_COMMAND, NEW_FIRM_COMMAND, LEXICON
from src.states.states import Category


