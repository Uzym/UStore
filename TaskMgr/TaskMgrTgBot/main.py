import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommandScopeDefault
from aiogram_dialog import setup_dialogs

from config import Config, load_config
from src.lexicon.lexicon import bot_lexicon, bot_description_lexicon, bot_short_description_lexicon
from src.services import UserService, SectionService, CardService, ProjectService, RoleService
from src.handlers import window_commands_router
from src.components import help_dialog, main_dialog, project_dialog, select_object_dialog, input_dialog, section_dialog, \
    card_dialog
from src.services.odata_service import MyODataService
from src.utils.window_builder import WindowBuilder

logger = logging.getLogger(__name__)


def init_services(dp: Dispatcher, config: Config):
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
    odata_service = MyODataService(api_key=config.api_key, logger=logger)
    dp["odata_service"] = odata_service


def setup_routers(dp: Dispatcher):
    dp.include_router(window_commands_router)

    dp.include_router(main_dialog)
    dp.include_router(help_dialog)
    dp.include_router(select_object_dialog)
    dp.include_router(input_dialog)
    dp.include_router(project_dialog)
    dp.include_router(section_dialog)
    dp.include_router(card_dialog)

    setup_dialogs(dp)


async def setup_bot_commands(bot: Bot, logger: logging.Logger):
    commands = []
    for builder in WindowBuilder.instances:
        if builder.command is None:
            continue
        logger.info(str(builder.command))
        commands.append(builder.command)

    await bot.set_my_commands(commands)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s "
        "[%(asctime)s] - %(name)s - %(message)s",
    )

    logger.info("Starting bot")

    config: Config = load_config()

    storage: MemoryStorage = MemoryStorage()

    bot: Bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    dp: Dispatcher = Dispatcher(storage=storage)

    init_services(dp=dp, config=config)
    setup_routers(dp=dp)

    try:
        await setup_bot_commands(bot, logger)
        await bot.set_my_name(str(bot_lexicon))
        await bot.set_my_description(str(bot_description_lexicon))
        await bot.set_my_short_description(str(bot_short_description_lexicon))
    except:
        logger.info("Don't init bot")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")