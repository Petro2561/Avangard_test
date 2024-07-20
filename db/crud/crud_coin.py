from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from db.crud.crud_base import CRUDBase
from db.db import Coin


class CRUDCoin(CRUDBase):
    async def get_coin_by_name(
        self, user_id: int, coin_name: str, session: AsyncSession
    ):
        db_obj = await session.execute(
            select(self.model)
            .where(self.model.user_id == user_id, self.model.coin_name == coin_name)
            .options(joinedload(self.model.user))
        )
        return db_obj.scalars().first()

    async def get_multi(self, session: AsyncSession):
        db_objs = await session.execute(
            select(self.model).options(joinedload(self.model.user))
        )
        return db_objs.scalars().all()


crud_coin = CRUDCoin(Coin)
