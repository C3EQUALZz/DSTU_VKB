from typing import cast
from uuid import uuid4

from typing_extensions import override

from chat_service.domain.chat.ports.chat_id_generator import ChatIDGenerator
from chat_service.domain.chat.values.chat_id import ChatID


class UUID4ChatIDGenerator(ChatIDGenerator):
    @override
    def __call__(self) -> ChatID:
        return cast(ChatID, uuid4())
