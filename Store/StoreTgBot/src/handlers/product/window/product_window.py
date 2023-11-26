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
from src.services import ProductService, PhotoService, S3Service
from src.states.states import Product

product_service = ProductService()
photo_service = PhotoService()
s3_service = S3Service()
logger = logging.getLogger()
token = config.load_config().tg_bot.token
bot = Bot(token)


async def get_product_photos(dialog_manager: DialogManager, **kwargs):
    dialog_manager.dialog_data["is_photo"] = None
    product_id = dialog_manager.dialog_data["product_id"]
    photo_objects = await photo_service.photos(product_id=product_id)
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


async def product_getter(dialog_manager: DialogManager, **kwargs):
    product_id = int(dialog_manager.start_data['product_id'])
    product_data = await product_service.get_product(product_id=product_id)
    photos = await get_product_photos(dialog_manager)
    return {
        "product_title": product_data.title,
        "product_description": product_data.description,
        "product_discount": product_data.discount,
        "product_cost": product_data.cost,
        "product_delivery_days":
            product_data.delivery_time.split('.')[0] if len(product_data.delivery_time.split('.')) else 0,
        "product_delivery_hours":
            product_data.delivery_time.split('.')[1].split(':')[0]
            if len(product_data.delivery_time.split('.')) > 1 else 0,
        "product_delivery_minutes": product_data.delivery_time.split('.')[1].split(':')[1],
        "product_delivery_seconds": product_data.delivery_time.split('.')[1].split(':')[2],
    }


async def get_product_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    await callback.answer(text=LEXICON["loading"])
    dialog_manager.start_data["product_id"] = item_id
    dialog_manager.dialog_data["product_id"] = item_id
    await dialog_manager.switch_to(Product.product)


async def to_product_update_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.product_update)


to_product_update_button = Button(
    text=Const(LEXICON["update"]),
    id="to_product_update",
    on_click=to_product_update_button
)


async def add_product_photo_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.product_wait_photo)


add_product_photo_button = Button(
    text=Const(LEXICON["add_photo"]),
    id="add_product_photo",
    on_click=add_product_photo_button
)


async def add_product_photo(message: Message, message_input: MessageInput, dialog_manager: DialogManager):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file = await bot.download_file(file_info.file_path)
    photo_data = await s3_service.upload_file(file_path=file_info.file_path, file=file)
    res = await photo_service.create_photo(name=photo_data.fileName, product_id=dialog_manager.dialog_data['product_id'])
    await dialog_manager.switch_to(Product.product)


product_wait_photo_window = Window(
    Const(LEXICON["send_photo"]),
    MessageInput(add_product_photo),
    state=Product.product_wait_photo
)


async def back_to_list_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    if 'title' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('title')
    if 'description' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('description')
    if 'discount' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('discount')
    if 'cost' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('cost')
    if 'delivery_time' in dialog_manager.dialog_data.keys():
        dialog_manager.dialog_data.pop('delivery_time')
    await dialog_manager.switch_to(Product.products)


back_to_list_button = Button(
    text=Const(LEXICON["back"]),
    id="back_to_products_list",
    on_click=back_to_list_button
)


async def product_photos_delete_button(callback: CallbackQuery, button: Button, dialog_manager: DialogManager, **kwargs):
    await dialog_manager.switch_to(Product.product_delete_photo)


product_photos_delete_button = Button(
    text=Const(LEXICON["delete_photo"]),
    id="product_photos_delete",
    on_click=product_photos_delete_button
)


async def delete_product_photo_button(callback: CallbackQuery, widget: Any, dialog_manager: DialogManager, item_id: str):
    photo_object = await photo_service.get_photo(photo_id=int(item_id))
    await s3_service.delete_file(file_name=photo_object.name)
    await photo_service.delete_photo(photo_id=photo_object.photo_id)
    await dialog_manager.switch_to(Product.product)


product_delete_photos_window = Window(
    Const(LEXICON["delete_photo"]),
    ScrollingGroup(
        Select(
            text=Format("{item[0]}"),
            item_id_getter=operator.itemgetter(1),
            items="photos",
            id="photo_i",
            when=F["dialog_data"]["is_photo"].is_not(None),
            on_click=delete_product_photo_button
        ),
        id="product_delete_photos_group",
        width=1,
        height=10,
    ),
    back_to_list_button,
    state=Product.product_delete_photo,
    getter=get_product_photos
)


product_window = Window(
    Const(LEXICON["product"]),
    Format(html.bold(html.quote("{product_title}"))),
    Format(html.quote("{product_description}")),
    Format(html.quote("Скидка: {product_discount}")),
    Format(html.quote("Цена: {product_cost} руб")),
    Format(html.quote("Время доставки: {product_delivery_days} дней {product_delivery_hours} "
                      "часов {product_delivery_minutes} минут {product_delivery_seconds} секунд")),
    add_product_photo_button,
    product_photos_delete_button,
    to_product_update_button,
    back_to_list_button,
    Cancel(Const(LEXICON["complete"])),
    state=Product.product,
    getter=product_getter
)
