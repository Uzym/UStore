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


# /new_product title; description; cost; category_title; series_title; delivery_time; discount + прикрепленные фото
@router.message(Command(commands=["new_product"]))
async def new_product(message: Message, command: CommandObject,
                      state: FSMContext, photo_service: PhotoService,
                      logger: Logger, product_service: ProductService,
                      series_service: SeriesService, category_service: CategoryService,
                      s3_service: S3Service):
    title, description, cost, category_title, series_title, delivery_time, discount = command.args.split("; ")
    try:

        category = await category_service.categories(title=category_title)
        series = await series_service.series_list(title=series_title)

        if len(category) < 1 or len(series) < 1:
            await message.answer("Не существует категории или серии")
            return

        product = await product_service.create_product(
            title=title,
            description=description,
            cost=float(cost),
            series_id=series[0].series_id,
            discount=float(discount),
            category_id=category[0].category_id,
            delivery_time=delivery_time
        )

        await message.answer(str(product))

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


# /new_category title; description; discount
@router.message(Command(commands=["new_category"]))
async def new_category(message: Message, command: CommandObject,
                      state: FSMContext, photo_service: PhotoService,
                      logger: Logger, product_service: ProductService,
                      series_service: SeriesService, category_service: CategoryService,
                      s3_service: S3Service):
    title, description, discount = command.args.split("; ")
    try:

        category = await category_service.create_category(
            title=title,
            description=description,
            discount=float(discount)
        )

        await message.answer(str(category))

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


# /new_series title; description; firm_title; discount
@router.message(Command(commands=["new_series"]))
async def new_series(message: Message, command: CommandObject,
                      state: FSMContext, photo_service: PhotoService,
                      logger: Logger, product_service: ProductService,
                      series_service: SeriesService, category_service: CategoryService,
                      s3_service: S3Service, firm_serivce: FirmService):
    title, description, firm_title, discount = command.args.split("; ")
    try:

        firm = await firm_serivce.firms(title=firm_title)

        if len(firm) < 1:
            await message.answer("Не существует фирмы")
            return

        series = await series_service.create_series(
            title=title,
            description=description,
            discount=float(discount),
            firm_id=firm[0].firm_id
        )

        await message.answer(str(series))

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


# /new_firm title; description; discount
@router.message(Command(commands=["new_firm"]))
async def new_firm(message: Message, command: CommandObject,
                      state: FSMContext, photo_service: PhotoService,
                      logger: Logger, product_service: ProductService,
                      series_service: SeriesService, category_service: CategoryService,
                      s3_service: S3Service, firm_serivce: FirmService):
    title, description, discount = command.args.split("; ")
    try:
        firm = await firm_serivce.create_firm(
            title=title,
            description=description,
            discount=float(discount)
        )

        await message.answer(str(firm))

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
