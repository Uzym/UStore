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
from src.services import CategoryService, PhotoService, S3Service
from src.states.states import Category

category_service = CategoryService()
photo_service = PhotoService()
s3_service = S3Service()
logger = logging.getLogger()
token = config.load_config().tg_bot.token
bot = Bot(token)


async def get_category_photos(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["is_photo"] = None
    category_id = dialog_manager.dialog_data["category_id"]
    photo_objects = await photo_service.photos(category_id=category_id)
    photos = []
    for photo_object in photo_objects:
        photo_bytes = await s3_service.download_file(file_name=photo_object.name)
        photo_file = BufferedInputFile(photo_bytes, filename=photo_object.name)
        photo = InputMediaPhoto(media=photo_file)
        photos.append(photo)
        dialog_manager.dialog_data["is_photo"] = True
    if len(photos) > 0:
        await bot.send_media_group(chat_id=dialog_manager.event.from_user.id, media=photos)
    photos_data = [
        (photo_object.name, str(photo_object.photo_id)) for photo_object in photo_objects
    ]
    return {
        "photos": photos_data
    }


async def category_getter(dialog_manager: DialogManager, **kwargs):
    category_id = int(dialog_manager.start_data['category_id'])
    category_data = await category_service.get_category(category_id=category_id)
    photos = await get_category_photos(dialog_manager)
    return {
        "category_title": category_data.title,
        "category_description": category_data.description,
        "category_discount": category_data.discount
    }


async def get_category_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data["category_id"] = item_id
    dialog_manager.dialog_data["category_id"] = item_id
    await dialog_manager.switch_to(Category.category)


async def to_category_update_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.category_update)


to_category_update_button = Button(
    text=Const(LEXICON["update"]),
    id="to_category_update",
    on_click=to_category_update_button
)


async def add_category_photo_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.category_wait_photo)


add_category_photo_button = Button(
    text=Const(LEXICON["add_photo"]),
    id="add_category_photo",
    on_click=add_category_photo_button
)


async def add_category_photo(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file = await bot.download_file(file_info.file_path)
    photo_data = await s3_service.upload_file(file_path=file_info.file_path, file=file)
    res = await photo_service.create_photo(name=photo_data.fileName, category_id=dialog_manager.dialog_data['category_id'])
    await dialog_manager.switch_to(Category.category)


category_wait_photo_window = Window(
    Const(LEXICON["send_photo"]),
    MessageInput(add_category_photo),
    state=Category.category_wait_photo
)


async def back_to_list_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    if 'title' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('title')
    if 'description' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('description')
    if 'discount' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('discount')
    await dialog_manager.switch_to(Category.categories)


back_to_list_button = Button(
    text=Const(LEXICON["back"]),
    id="back_to_categories_list",
    on_click=back_to_list_button
)


async def category_photos_delete_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Category.category_delete_photo)


category_photos_delete_button = Button(
    text=Const(LEXICON["delete_photo"]),
    id="category_photos_delete",
    on_click=category_photos_delete_button
)


async def delete_category_photo_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    photo_object = await photo_service.get_photo(photo_id=int(item_id))
    await s3_service.delete_file(file_name=photo_object.name)
    await photo_service.delete_photo(photo_id=photo_object.photo_id)
    await dialog_manager.switch_to(Category.category)


category_delete_photos_window = Window(
    Const(LEXICON["delete_photo"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="photos",
            id="photo_i",
            when=F["dialog_data"]["is_photo"].is_not(None),
            on_click=delete_category_photo_button
        ),
        id="category_delete_photos_group",
        width=1,
        height=10,
    ),
    back_to_list_button,
    state=Category.category_delete_photo,
    getter=get_category_photos
)


category_window = Window(
    Const(LEXICON["category"]),
    Format(html.bold(html.quote("{category_title}"))),
    Format(html.quote("{category_description}")),
    Format(html.quote("{category_discount}")),
    add_category_photo_button,
    category_photos_delete_button,
    to_category_update_button,
    back_to_list_button,
    Cancel(Const(LEXICON["complete"])),
    state=Category.category,
    getter=category_getter
)