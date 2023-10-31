from logging import Logger

from config import config
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType, BufferedInputFile, InputFile
from src.lexicon import LEXICON
from aiogram.filters import Command
from typing import List
from src.services import FirmService, PhotoService, S3Service
from aiogram import Bot
from io import BytesIO

router: Router = Router()

token = config.load_config().tg_bot.token
bot = Bot(token)


@router.message(Command(commands=["start"]))
async def start_message(message: Message, state: FSMContext, photo_service: PhotoService, logger: Logger):
    res = await photo_service.photos(product_id=None, firm_id=None, category_id=None, series_id=None)
    logger.info(str(res))
    await message.answer(text=str(res))


@router.message(F.content_type.in_({'photo'}))
async def photo_upload(message: Message, s3_service: S3Service, logger: Logger):
    file_id = message.photo[-1].file_id
    file_info = await bot.get_file(file_id)
    file = await bot.download_file(file_info.file_path)
    res = await s3_service.upload_file(file_path=file_info.file_path, file=file)
    logger.info(res)
    await message.reply(str(res))


@router.message(F.content_type.in_({'text'}))
async def photo_upload(message: Message, s3_service: S3Service, logger: Logger):
    logger.info(message.text)
    file_bytes = await s3_service.download_file(file_name=message.text)
    photo = BufferedInputFile(file_bytes, filename=message.text)
    await message.answer_photo(photo=photo)
