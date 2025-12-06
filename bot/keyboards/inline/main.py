from __future__ import annotations

from typing import TYPE_CHECKING

from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.enums import Locale, UserProfile

from .factory import Language, Pagination, Profile


if TYPE_CHECKING:
    from aiogram.types import InlineKeyboardMarkup
    from aiogram_i18n import I18nContext



def select_language() -> InlineKeyboardMarkup:
    """
    Select language keyboard

    :return: InlineKeyboardMarkup with language selection
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.row(
        InlineKeyboardButton(
            text="🇮🇷 فارسی",
            callback_data=Language(language=Locale.FA).pack(),
        ),
        InlineKeyboardButton(
            text="🇬🇧 English",
            callback_data=Language(language=Locale.EN).pack(),
        ),
        width=2,
    )
    return keyboard.as_markup()


def pagination_users(*, end_page: bool = False, page: int = 0) -> InlineKeyboardMarkup:
    """
    Pagination keyboard for top users.

    :param end_page: Is the last page.
    :param page: Page number (zero-based).
    :return: InlineKeyboardMarkup with the top users pagination controls.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    # Previous page button
    if page > 0:
        prev_text = "◀️"
        prev_page = page - 1
    else:
        # Already at the first page, keep the same page index
        prev_text = "🍓"
        prev_page = page

    prev_callback = Pagination(page=prev_page, action="PREV_USER").pack()

    # Next page button
    if not end_page:
        next_text = "▶️"
        next_page = page + 1
    else:
        # Already at the last page, keep the same page index
        next_text = "🍑"
        next_page = page

    next_callback = Pagination(page=next_page, action="NEXT_USER").pack()

    keyboard.row(
        InlineKeyboardButton(text=prev_text, callback_data=prev_callback),
        InlineKeyboardButton(text="👤", callback_data=UserProfile.HOME),
        InlineKeyboardButton(text=next_text, callback_data=next_callback),
        width=3,
    )
    return keyboard.as_markup()


def profile(i18n: I18nContext, *, profile: bool) -> InlineKeyboardMarkup:
    """
    Open profile keyboard

    :param i18n: I18nContext object.
    :param profile: Is the profile opened.
    :return: InlineKeyboardMarkup with the open profile button.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()

    if profile:
        keyboard.add(
            InlineKeyboardButton(
                text=i18n.get("close-profile-btn"),
                callback_data=Profile(action=UserProfile.CLOSE).pack(),
            ),
        )
    else:
        keyboard.add(
            InlineKeyboardButton(
                text=i18n.get("profile-btn"),
                callback_data=Profile(action=UserProfile.OPEN).pack(),
            ),
        )
    keyboard.adjust(1)
    return keyboard.as_markup()


def link_profile(i18n: I18nContext, url: str) -> InlineKeyboardMarkup:
    """
    Link profile keyboard

    :param i18n: I18nContext object.
    :param url: URL of the profile.
    :return: InlineKeyboardMarkup with the link to the profile.
    """
    keyboard: InlineKeyboardBuilder = InlineKeyboardBuilder()
    keyboard.add(InlineKeyboardButton(text=i18n.get("profile-btn"), url=url))
    return keyboard.as_markup()
