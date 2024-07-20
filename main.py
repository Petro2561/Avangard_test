import asyncio
import logging

from aiogram import Bot, Dispatcher, Router
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from bot.config import Config, load_config
from bot.handlers import router
from bot.middleware import SaveUserMiddleware
from bot.sheduler import check_prices
from db.db import create_tables

CHECK_INTERVAL = 60  # Check every 60 seconds

logging.basicConfig(level=logging.INFO)


# @router.message(Command("set"))
# async def set_alert_command(message: Message):
#     args = message.text.split()
#     if len(args) != 4:
#         await message.answer("Использование: /set <currency> <min_threshold> <max_threshold>")
#         return

#     currency = args[1].upper()
#     try:
#         min_threshold = float(args[2])
#         max_threshold = float(args[3])
#     except ValueError:
#         await message.answer("Пороговые значения должны быть числами.")
#         return

#     chat_id = message.chat.id
#     if chat_id not in alerts:
#         alerts[chat_id] = []
#     alerts[chat_id].append({'currency': currency, 'min': min_threshold, 'max': max_threshold})
#     await message.answer(f'Оповещение установлено для {currency}: мин {min_threshold}, макс {max_threshold}')


async def main():
    config: Config = load_config()
    bot = Bot(token=config.tg_bot.token)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    scheduler = AsyncIOScheduler()
    dp.message.middleware(SaveUserMiddleware())
    dp.include_router(router)
    await create_tables()
    scheduler.add_job(check_prices, IntervalTrigger(seconds=CHECK_INTERVAL), args=[bot])
    scheduler.start()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
