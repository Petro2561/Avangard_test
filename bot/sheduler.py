from api.api_request import get_coin_price
from db.crud.crud_coin import crud_coin
from db.db import get_async_session
from aiogram import Bot

ERROR_MESSAGE = 'Не удается получится цену по валюте {coin_name}. Возможно такой валюты не существует.'

async def check_prices(bot: Bot):
    async for session in get_async_session():
        coins = await crud_coin.get_multi(session)
        for coin in coins:
            try:
                price = await get_coin_price(coin.coin_name)
                if price <= coin.min_price or price >= coin.max_price:
                    message = f"Цена {coin.coin_name} достигла {price:.2f} USD!"
                    await bot.send_message(coin.user.telegram_id, message)
            except KeyError:
                   await bot.send_message(coin.user.telegram_id, ERROR_MESSAGE.format(coin_name=coin.coin_name))
