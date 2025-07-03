import logging
from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.fsm.context import FSMContext
from aiogram.types import TelegramObject, User
from psycopg import AsyncConnection

from app.infrastructure.database.db import get_user_lang, get_user, add_user

logger = logging.getLogger(__name__)


class TranslatorMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any],
    ) -> Any:
        user: User = data.get("event_from_user")
        if user is None:
            return await handler(event, data)

        state: FSMContext = data.get('state')
        user_context_data = await state.get_data()

        if (user_lang := user_context_data.get('user_lang')) is None:
            conn: AsyncConnection = data.get("conn")
            if conn is None:
                logger.error("Database connection not found in middleware data.")
                raise RuntimeError("Missing database connection for detecting the user's language.")

            # Проверяем, существует ли пользователь в БД
            existing_user = await get_user(conn, user_id=user.id)
            if existing_user is None:
                # Создаем пользователя, если его нет
                await add_user(
                    conn,
                    user_id=user.id,
                    username=user.username,
                    language=user.language_code or "ru",  # используем язык из Telegram или "ru" по умолчанию
                )
                user_lang = user.language_code or "ru"
                logger.info(f"Auto-created user {user.id} ({user.username}) with language {user_lang}")
            else:
                user_lang: str | None = await get_user_lang(conn, user_id=user.id)
                if user_lang is None:
                    user_lang = user.language_code or "ru"

        translations: dict = data.get("translations")

        # Добавляем проверку на None
        if translations is None:
            logger.error("Translations not found in middleware data.")
            # Устанавливаем пустой i18n или значение по умолчанию
            data["i18n"] = {}
            return await handler(event, data)

        i18n: dict = translations.get(user_lang)
        if i18n is None:
            # Проверяем, есть ли default ключ
            default_lang = translations.get("default")
            if default_lang and default_lang in translations:
                data["i18n"] = translations[default_lang]
            else:
                # Берем первый доступный язык или пустой словарь
                available_langs = [k for k in translations.keys() if k != "default"]
                if available_langs:
                    data["i18n"] = translations[available_langs[0]]
                else:
                    data["i18n"] = {}
                logger.warning(f"Language {user_lang} not found in translations, using fallback")
        else:
            data["i18n"] = i18n

        return await handler(event, data)
