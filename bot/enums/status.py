
from enum import StrEnum, auto


class UserStatus(StrEnum):
    """
    Enumeration representing user statuses.
    """

    FREE = auto()
    WAITING = auto()
    CHATTING = auto()

    DEFAULT = FREE
