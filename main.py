import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot.config import Config, load_config
from bot.handlers import router
from bot.middleware import SaveUserMiddleware, DbSessionMiddleware
from bot.sheduler import check_prices
from db.create_pool import create_pool

CHECK_INTERVAL = 60

async def main():
    logging.basicConfig(level=logging.INFO)
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler()
    session_pool = await create_pool()
    dp.message.middleware(DbSessionMiddleware(session_pool))
    dp.message.middleware(SaveUserMiddleware())
    dp.include_router(router)
    scheduler.add_job(check_prices, IntervalTrigger(seconds=CHECK_INTERVAL), args=[bot])
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
