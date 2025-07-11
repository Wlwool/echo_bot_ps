import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from psycopg import AsyncConnection

from app.infrastructure.database.db import get_user_banned_status_by_id

logger = logging.getLogger(__name__)


class ShadowBanMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")

        if user is None:
            return await handler(event, data)

        conn: AsyncConnection = data.get("conn")
        if conn is None:
            logger.error("Database connection not found in middleware data.")
            raise RuntimeError("Missing database connection for shadow ban check.")

        try:
            user_banned_status = await get_user_banned_status_by_id(
                conn, user_id=user.id
            )
            if user_banned_status:
                logger.warning("Shadow-banned user tried to interact: %d", user.id)
                if hasattr(event, "callback_query") and event.callback_query:
                    await event.callback_query.answer()
                return
        except Exception as e:
            logger.error(f"Error in shadow ban check: {e}")

        return await handler(event, data)
