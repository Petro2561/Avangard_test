from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from db.crud.crud_user import crud_user
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


class DbSessionMiddleware(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)
        
        
class SaveUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        user = await crud_user.get_user_by_telegram_id(event.from_user.id, data["session"])
        if not user:
            user_data = {
                "telegram_id": event.from_user.id,
                "username": event.from_user.username,
                "full_name": event.from_user.full_name,
            }
            user = await crud_user.create(obj_in=user_data, session=data["session"])
        data["user"] = user
        return await handler(event, data)