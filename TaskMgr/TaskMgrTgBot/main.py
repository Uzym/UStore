import asyncio
import logging

from aiogram import Bot, Dispatcher

from config import Config, load_config
from src.services import UserService, SectionService, CardService, ProjectService, RoleService
from src.handlers import common_router, project_router, section_router

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

    role_service = RoleService(api_key=config.api_key, logger=logger)
    dp["role_service"] = role_service
    card_service = CardService(api_key=config.api_key, logger=logger)
    dp["card_service"] = card_service
    section_service = SectionService(api_key=config.api_key, card_service=card_service, logger=logger)
    dp["section_service"] = section_service
    user_service = UserService(api_key=config.api_key)
    dp["user_service"] = user_service
    project_service = ProjectService(api_key=config.api_key, logger=logger)
    dp["project_service"] = project_service

    dp["logger"] = logger

    dp.include_router(common_router)
    dp.include_router(project_router)
    dp.include_router(section_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")