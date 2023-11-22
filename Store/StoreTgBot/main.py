import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from config import Config, load_config
from src.lexicon import COMMANDS
from src.lexicon.lexicon import BOT_NAME, BOT_DESCRIPTION, BOT_SHORT_DESCRIPTION
from src.services import (FirmService, PhotoService, ProductService, CategoryService, SeriesService, UserService,
                          OrderService)
from src.services import S3Service
from src.handlers import main_setup, firm_setup, category_setup, series_setup, product_setup

logger = logging.getLogger(__name__)


def init_services(dp: Dispatcher, config: Config):
    user_service = UserService(api_key=config.api_key, logger=logger)
    dp["user_service"] = user_service
    firm_service = FirmService(api_key=config.api_key, logger=logger)
    dp["firm_service"] = firm_service
    photo_service = PhotoService(api_key=config.api_key, logger=logger)
    dp["photo_service"] = photo_service
    product_service = ProductService(api_key=config.api_key, logger=logger)
    dp["product_service"] = product_service
    category_service = CategoryService(api_key=config.api_key, logger=logger)
    dp["category_service"] = category_service
    series_service = SeriesService(api_key=config.api_key, logger=logger)
    dp["series_service"] = series_service
    order_service = OrderService(api_key=config.api_key, logger=logger)
    dp["order_service"] = order_service
    s3_service = S3Service(api_key=config.s3_api_key, logger=logger)
    dp["s3_service"] = s3_service


def setup_routers(dp: Dispatcher):
    main_router, main_dialog = main_setup()
    firm_router, firm_dialog = firm_setup()
    category_router, category_dialog = category_setup()
    series_router, series_dialog = series_setup()
    product_router, product_dialog = product_setup()

    dp.include_router(main_router)
    dp.include_router(firm_router)
    dp.include_router(category_router)
    dp.include_router(series_router)
    dp.include_router(product_router)

    dp.include_router(main_dialog)
    dp.include_router(firm_dialog)
    dp.include_router(category_dialog)
    dp.include_router(series_dialog)
    dp.include_router(product_dialog)

    setup_dialogs(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
               "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher()

    init_services(dp, config)
    dp["logger"] = logger
    setup_routers(dp)
    try:
        await bot.set_my_name(BOT_NAME)
        await bot.set_my_description(BOT_DESCRIPTION)
        await bot.set_my_short_description(BOT_SHORT_DESCRIPTION)
        await bot.set_my_commands(COMMANDS)
    except:
        logger.info("Don't init bot")

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
