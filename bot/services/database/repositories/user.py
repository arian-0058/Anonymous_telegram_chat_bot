from __future__ import annotations

import secrets
from typing import TYPE_CHECKING, Optional, cast

from sqlalchemy import and_, func, select

from bot.enums import UserStatus
from bot.services.database.models import DBUser


if TYPE_CHECKING:
    from sqlalchemy import Result, Select

from .base import BaseRepository


class UserRepository(BaseRepository):
    """
    The repository for the users.
    """

    async def get(self, user_id: int) -> DBUser | None:
        """
        Get a user by their ID.

        :param user_id: The user's ID.
        :return: The user, if found.
        """
        return cast(
            Optional[DBUser],
            await self._session.scalar(select(DBUser).where(DBUser.id == user_id)),
        )

    async def get_random_companion(self, user_id: int) -> DBUser | None:
        """
        Get a random companion for the user.

        :param user: The user's ID.
        :return: The companion's ID, if found.
        """
        query: Select[tuple[int]] = select(DBUser.id).where(
            and_(DBUser.status == UserStatus.WAITING, DBUser.id != user_id),
        )
        result: Result[tuple[int]] = await self._session.execute(query)
        companions: list[int] | None = list(result.scalars().all())
        companion: int | None = secrets.choice(companions) if companions else None

        return cast(Optional[DBUser], await self.get(user_id=companion))

    async def update_companions(
        self,
        user: DBUser,
        companion: DBUser,
        user_status: UserStatus,
        companion_status: UserStatus,
        is_stop: bool | None = False,
    ) -> None:
        """
        Update the companions.

        :param user: The user.
        :param companion: The companion.
        :param user_status: The user's status.
        :param companion_status: The companion's status.
        :param is_stop: Whether the user stopped the conversation.
        """
        user.companion, companion.companion = (None, None) if is_stop else (companion.id, user.id)
        user.status, companion.status = user_status.value, companion_status.value




