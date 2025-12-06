from __future__ import annotations

from typing import TYPE_CHECKING, Final

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardRemove

from bot.keyboards.inline import Language, select_language
from bot.utils import set_commands


if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import CallbackQuery, Message
    from aiogram_i18n import I18nContext

    from bot.services.database import DBUser


router: Final[Router] = Router(name=__name__)


@router.message(Command("language"), flags={"throttling_key": "default"})
async def language_command(message: "Message", i18n: "I18nContext", user: "DBUser") -> None:
    """Handle /language command: show language selection keyboard."""
    await message.answer(
        text=i18n.get("language", name=user.mention),
        reply_markup=select_language(),
    )


@router.callback_query(Language.filter(), flags={"throttling_key": "default"})
async def language_changed(
    callback: "CallbackQuery",
    callback_data: "Language",
    bot: "Bot",
    i18n: "I18nContext",
    user: "DBUser",
) -> None:
    """Handle language change from inline keyboard."""
    # Update locale in storage
    await i18n.set_locale(locale=callback_data.language)
    # Reset localized commands for this chat
    await set_commands(bot=bot, i18n=i18n, chat_id=user.id)

    # Small toast notification
    await callback.answer(i18n.get("language-changed"))

    # Replace keyboard message with fresh /help in new language
    if callback.message:
        await callback.message.delete()
        await callback.message.answer(
            text=i18n.get("help", name=user.mention),
            reply_markup=ReplyKeyboardRemove(),
        )
