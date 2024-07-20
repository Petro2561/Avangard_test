from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from db.crud.crud_user import crud_user
from db.db import get_async_session


class SaveUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        async for session in get_async_session():
            user = await crud_user.get_user_by_telegram_id(event.from_user.id, session)
            if not user:
                user_data = {
                    "telegram_id": event.from_user.id,
                    "username": event.from_user.username,
                    "full_name": event.from_user.full_name,
                }
                user = await crud_user.create(obj_in=user_data, session=session)
            data["user"] = user  # Adding user to data for further use in handlers
        return await handler(event, data)
