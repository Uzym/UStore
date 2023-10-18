from aiogram import Bot, Dispatcher, types
from aiogram.fsm.strategy import FSMStrategy
from aiogram.fsm.storage.memory import MemoryStorage
import logging
import asyncio
import os

# from app.handlers import common, consume, manage
# from app.config import config

# logger = logging.getLogger(__name__)

# async def main() -> None:

#     asyncio.set_event_loop(config.loop)

#     logging.basicConfig(
#         level=logging.INFO,
#         format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
#     )
#     logger.info("Starting bot")

#     dp = Dispatcher(storage=MemoryStorage(), fsm_strategy=FSMStrategy.USER_IN_CHAT)

#     dp.include_router(manage.router)
#     dp.include_router(common.router)
#     dp.include_router(consume.router)

#     try:
#         await dp.start_polling(config.bot, allowed_updates=dp.resolve_used_update_types())
#     finally:
#         await config.bot.session.close()

# if __name__ == '__main__':
#     config.loop.run_until_complete(main())