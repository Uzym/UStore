# from logging import Logger

# from config import config
# from aiogram import Router, F
# from aiogram.fsm.context import FSMContext
# from aiogram.types import Message, ContentType, BufferedInputFile, InputFile
# from src.lexicon import LEXICON
# from aiogram.filters import Command, CommandObject
# from typing import List
# from src.services import FirmService, PhotoService, S3Service, ProductService, SeriesService, CategoryService
# from aiogram import Bot
# from io import BytesIO

# router: Router = Router()

# token = config.load_config().tg_bot.token
# bot = Bot(token)


# @router.message(Command(commands=["search"]))
# async def search(message: Message, command: CommandObject,
#                  state: FSMContext, photo_service: PhotoService,
#                  logger: Logger, product_service: ProductService,
#                  series_service: SeriesService, category_service: CategoryService,
#                  s3_service: S3Service, firm_service: FirmService):
#     table, title = command.args.split("; ")
#     logger.info(command.args)
#     try:
#         data = []
#         if table == "product":
#             data = await product_service.products(title=title)
#         elif table == "firm":
#             data = await firm_service.firms(title=title)
#         elif table == "series":
#             data = await series_service.series_list(title=title)
#         elif table == "category":
#             data = await category_service.categories(title=title)
#         logger.info(data)
#         await message.answer(
#             text=''.join(str(data))
#         )
#     except:
#         await message.answer("Ошибка")
