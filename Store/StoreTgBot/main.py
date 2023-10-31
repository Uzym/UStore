import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config, load_config

from src.services import FirmService, PhotoService, ProductService, CategoryService, UserService, OrderService
from src.services import S3Service
from src.handlers import common_router

logger = logging.getLogger(__name__)


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
    order_service = OrderService(api_key=config.api_key, logger=logger)
    dp["order_service"] = order_service

    s3_service = S3Service(api_key=config.s3_api_key, logger=logger)
    dp["s3_service"] = s3_service

    dp["logger"] = logger

    dp.include_router(common_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")