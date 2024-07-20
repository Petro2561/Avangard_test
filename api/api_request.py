import asyncio

import aiohttp

from bot.config import Config, load_config

config: Config = load_config()


async def get_coin_price(currency: str) -> int:
    url = f"https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={currency}&convert=USD"
    headers = {"X-CMC_PRO_API_KEY": config.api.api_token}

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            response_json = await response.json()
            try:
                return response_json["data"][currency]["quote"]["USD"]["price"]
            except KeyError:
                raise KeyError
