from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.enums import ParseMode


if TYPE_CHECKING:
    from bot.config import Config


def create_bot(config: Config) -> Bot:
    """
    Creates a Telegram bot instance.
    """

    # پروکسی v4freedom - HTTP proxy port = 10811
    proxy_url = "http://127.0.0.1:10811"

    session = AiohttpSession(proxy=proxy_url)

    return Bot(
        token=config.bot_token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        session=session,  # استفاده از سشن پروکسی‌دار
    )
