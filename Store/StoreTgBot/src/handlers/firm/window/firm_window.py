import operator
import logging

from typing import Any
from config import config
from aiogram.types import CallbackQuery, Message, BufferedInputFile, ContentType, InputMediaPhoto
from aiogram import html, Bot, F
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Select, Group, ScrollingGroup, Button, Row, Cancel, Back
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.media import DynamicMedia

from src.lexicon import LEXICON
from src.services import FirmService, PhotoService, S3Service
from src.states.states import Firm

firm_service = FirmService()
photo_service = PhotoService()
s3_service = S3Service()
logger = logging.getLogger()
token = config.load_config().tg_bot.token
bot = Bot(token)


async def get_firm_photos(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["is_photo"] = None
    firm_id = dialog_manager.dialog_data['firm_id']
    photo_objects = await photo_service.photos(firm_id=firm_id)
    photos = []
    for photo_object in photo_objects:
        photo_bytes = await s3_service.download_file(file_name=photo_object.name)
        photo_file = BufferedInputFile(photo_bytes, filename=photo_object.name)
        photo = InputMediaPhoto(media=photo_file)
        photos.append(photo)
        dialog_manager.dialog_data["is_photo"] = True
    if len(photos) > 0:
        await bot.send_media_group(chat_id=dialog_manager.event.from_user.id, media=photos)
    return {
        'photos': photos
    }


async def firm_getter(dialog_manager: DialogManager, **kwargs):
    firm_id = int(dialog_manager.start_data['firm_id'])
    firm_data = await firm_service.get_firm(firm_id=firm_id)
    photos = await get_firm_photos(dialog_manager)
    return {
        "firm_title": firm_data.title,
        "firm_description": firm_data.description,
        "firm_discount": firm_data.discount,
        "photos": photos["photos"]
    }


async def get_firm_button(callback: CallbackQuery, widget: Any, manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    manager.start_data['firm_id'] = item_id
    manager.dialog_data['firm_id'] = item_id
    await manager.switch_to(Firm.firm)


async def to_firm_update_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firm_update)


to_firm_update_button = Button(
    text=Const("Изменить"),
    id="firms_update_go_back",
    on_click=to_firm_update_button
)


async def add_firm_photo_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    await manager.switch_to(Firm.firm_wait_photo)


add_firm_photo_button = Button(
    text=Const("Добавить фото"),
    id="add_firm_photo",
    on_click=add_firm_photo_button
)


async def add_firm_photo(message: Message, message_input: MessageInput, manager: DialogManager):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file = await bot.download_file(file_info.file_path)
    photo_data = await s3_service.upload_file(file_path=file_info.file_path, file=file)
    logger.info(photo_data)
    res = await photo_service.create_photo(name=photo_data.fileName, firm_id=manager.dialog_data['firm_id'])
    logger.info(res)
    await manager.switch_to(Firm.firm)


firm_wait_photo_window = Window(
    Const("Отправьте фото (как фото а не как файл)"),
    MessageInput(add_firm_photo),
    state=Firm.firm_wait_photo
)


async def back_to_list_button(callback: CallbackQuery, button: Button, manager: DialogManager, **kwargs):
    if 'title' in manager.dialog_data.keys():
        manager.dialog_data.pop('title')
    if 'description' in manager.dialog_data.keys():
        manager.dialog_data.pop('description')
    if 'discount' in manager.dialog_data.keys():
        manager.dialog_data.pop('discount')
    await manager.switch_to(Firm.firms)


back_to_list_button = Button(
    text=Const(LEXICON["back"]),
    id="back_to_firms_list",
    on_click=back_to_list_button
)


firm_window = Window(
    Format("Фирма"),
    # DynamicMedia("photos", when=F["dialog_data"]["is_photo"].is_not(None)),
    Format(html.bold(html.quote("{firm_title}"))),
    Format(html.quote("{firm_description}")),
    Format(html.quote("{firm_discount}")),
    add_firm_photo_button,
    to_firm_update_button,
    back_to_list_button,
    Cancel(Const("Завершить")),
    state=Firm.firm,
    getter=firm_getter
)