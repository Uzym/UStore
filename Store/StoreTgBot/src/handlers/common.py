from logging import Logger

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ContentType
from src.lexicon import LEXICON
from aiogram.filters import Command
from typing import List
from src.services import FirmService, PhotoService, S3Service

router: Router = Router()


@router.message(Command(commands=["start"]))
async def start_message(message: Message, state: FSMContext, photo_service: PhotoService, logger: Logger):
    res = await photo_service.photos(product_id=None, firm_id=None, category_id=None, series_id=None)
    logger.info(str(res))
    await message.answer(text=str(res))


# @router.message() TODO написать
# async def photo_upload(message: Message, s3_service: S3Service):
#     await message.reply(message.photo[-1].file_id)
#     # res = await s3_service
