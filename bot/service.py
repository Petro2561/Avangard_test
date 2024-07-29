from db.db import Coin, User, get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from db.crud.crud_coin import crud_coin
from db.crud.crud_user import crud_user


async def create_or_update_coin(data: dict, telegram_id: int, session: AsyncSession):
    user: User = await crud_user.get_user_by_telegram_id(telegram_id=telegram_id, session=session)
    coin: Coin = await get_coin_by_name(coin_name=data['coin_name'], user_id=user.id, session=session)
    coin_data = {
        'coin_name': data['coin_name'],
        'min_price': data['min_price'],
        'max_price': data['max_price'],
        'user_id': user.id
    }
    if coin:
        await crud_coin.update(coin, coin_data, session)
    else:
        await crud_coin.create(obj_in=coin_data, session=session)

async def get_coin_by_name(coin_name: str, user_id: int, session: AsyncSession):
    return await crud_coin.get_coin_by_name(coin_name=coin_name, user_id=user_id, session=session)


