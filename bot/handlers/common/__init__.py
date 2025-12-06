# File: bot/handlers/common/__init__.py
# Section: whole file

from typing import Final

from aiogram import Router

from . import dialog, language, profile, start


router: Final[Router] = Router(name=__name__)
router.include_routers(
    start.router,
    language.router,
    profile.router,
    dialog.router,
)
