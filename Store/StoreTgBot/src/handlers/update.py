from logging import Logger

from config import config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, BufferedInputFile, InputFile
from src.lexicon import LEXICON
from aiogram.filters import Command, CommandObject
from typing import List
from src.services import FirmService, PhotoService, S3Service, ProductService, SeriesService, CategoryService
from aiogram import Bot
from io import BytesIO

router: Router = Router()

token = config.load_config().tg_bot.token
bot = Bot(token)


# /update_product product_id; title; description; cost; category_title; series_title; delivery_time; discount + прикрепленные фото
@router.message(Command(commands=["update_product"]))
async def new_product(message: Message, command: CommandObject,
                      state: FSMContext, photo_service: PhotoService,
                      logger: Logger, product_service: ProductService,
                      series_service: SeriesService, category_service: CategoryService,
                      s3_service: S3Service):
    product_id, title, description, cost, category_title, series_title, delivery_time, discount = command.args.split("; ")
    try:

        category = await category_service.categories(title=category_title)
        series = await series_service.series_list(title=series_title)

        if len(category) < 1 or len(series) < 1:
            await message.answer("Не существует категории или серии")
            return

        product = await product_service.update_product(
            product_id=int(product_id),
            title=title,
            description=description,
            cost=float(cost),
            series_id=series[0].series_id,
            discount=float(discount),
            category_id=category[0].category_id,
            delivery_time=delivery_time
        )

        await message.answer(str(product))

        await message.answer("Удаление старых фото... Ждите")
        old_photos = await photo_service.photos(product_id=int(product_id))
        for old in old_photos:
            await photo_service.delete_photo(photo_id=old.photo_id)
            await s3_service.delete_file(file_name=old.name)
            await message.answer(text=f"Удалено {old.name}")

        await message.answer("Добавление фото... Ждите")
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file = await bot.download_file(file_info.file_path)
        photo = await s3_service.upload_file(file_path=file_info.file_path, file=file)

        photo_res = await photo_service.create_photo(
            name=photo.fileName,
            product_id=product.product_id
        )

        await message.answer(str(photo_res))
    except:
        await message.answer("Ошибка")


# /update_category category_id; title; description; discount + прикрепленные фото
@router.message(Command(commands=["update_category"]))
async def update_category(message: Message, command: CommandObject,
                          state: FSMContext, photo_service: PhotoService,
                          logger: Logger, product_service: ProductService,
                          series_service: SeriesService, category_service: CategoryService,
                          s3_service: S3Service):
    category_id, title, description, discount = command.args.split("; ")
    try:

        category = await category_service.update_category(
            category_id=int(category_id),
            title=title,
            description=description,
            discount=float(discount)
        )

        await message.answer(str(category))

        await message.answer("Удаление старых фото... Ждите")
        old_photos = await photo_service.photos(category_id=category_id)
        for old in old_photos:
            await photo_service.delete_photo(photo_id=old.photo_id)
            await s3_service.delete_file(file_name=old.name)
            await message.answer(text=f"Удалено {old.name}")

        await message.answer("Добавление фото... Ждите")
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file = await bot.download_file(file_info.file_path)
        photo = await s3_service.upload_file(file_path=file_info.file_path, file=file)

        photo_res = await photo_service.create_photo(
            name=photo.fileName,
            category_id=category.category_id
        )

        await message.answer(str(photo_res))
    except:
        await message.answer("Ошибка")


# /update_series series_id; title; description; firm_title; discount + прикрепленные фото
@router.message(Command(commands=["new_series"]))
async def update_series(message: Message, command: CommandObject,
                      state: FSMContext, photo_service: PhotoService,
                      logger: Logger, product_service: ProductService,
                      series_service: SeriesService, category_service: CategoryService,
                      s3_service: S3Service, firm_serivce: FirmService):
    series_id, title, description, firm_title, discount = command.args.split("; ")
    try:

        firm = await firm_serivce.firms(title=firm_title)

        if len(firm) < 1:
            await message.answer("Не существует фирмы")
            return

        series = await series_service.update_series(
            series_id=int(series_id),
            title=title,
            description=description,
            discount=float(discount),
            firm_id=firm[0].firm_id
        )

        await message.answer(str(series))

        await message.answer("Удаление старых фото... Ждите")
        old_photos = await photo_service.photos(series_id=series_id)
        for old in old_photos:
            await photo_service.delete_photo(photo_id=old.photo_id)
            await s3_service.delete_file(file_name=old.name)
            await message.answer(text=f"Удалено {old.name}")

        await message.answer("Добавление фото... Ждите")
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file = await bot.download_file(file_info.file_path)
        photo = await s3_service.upload_file(file_path=file_info.file_path, file=file)

        photo_res = await photo_service.create_photo(
            name=photo.fileName,
            series_id=series.series_id
        )

        await message.answer(str(photo_res))
    except:
        await message.answer("Ошибка")


# /update_firm firm_id; title; description; discount + прикрепленные фото
@router.message(Command(commands=["update_firm"]))
async def new_firm(message: Message, command: CommandObject,
                      state: FSMContext, photo_service: PhotoService,
                      logger: Logger, product_service: ProductService,
                      series_service: SeriesService, category_service: CategoryService,
                      s3_service: S3Service, firm_serivce: FirmService):
    firm_id, title, description, discount = command.args.split("; ")
    try:
        firm = await firm_serivce.update_firm(
            firm_id=int(firm_id),
            title=title,
            description=description,
            discount=float(discount)
        )

        await message.answer(str(firm))

        await message.answer("Удаление старых фото... Ждите")
        old_photos = await photo_service.photos(firm_id=firm_id)
        for old in old_photos:
            await photo_service.delete_photo(photo_id=old.photo_id)
            await s3_service.delete_file(file_name=old.name)
            await message.answer(text=f"Удалено {old.name}")

        await message.answer("Добавление фото... Ждите")
        file_id = message.photo[-1].file_id
        file_info = await bot.get_file(file_id)
        file = await bot.download_file(file_info.file_path)
        photo = await s3_service.upload_file(file_path=file_info.file_path, file=file)

        photo_res = await photo_service.create_photo(
            name=photo.fileName,
            firm_id=firm.firm_id
        )

        await message.answer(str(photo_res))
    except:
        await message.answer("Ошибка")
