from typing import Final, Iterable

from aiogram.enums import ChatType
from aiogram.filters import BaseFilter
from aiogram.types import Message
from typing_extensions import override


class ChatTypeFilter(BaseFilter):
    def __init__(self, allowed_chat_types: Iterable[ChatType]) -> None:
        self._allowed_chat_types: Final[Iterable[ChatType]] = allowed_chat_types

    @override
    async def __call__(self, message: Message) -> bool:
        return message.chat.type in self._allowed_chat_types