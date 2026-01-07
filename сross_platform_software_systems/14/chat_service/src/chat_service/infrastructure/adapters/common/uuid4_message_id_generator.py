from typing import cast
from uuid import uuid4

from typing_extensions import override

from chat_service.domain.chat.ports.message_id_generator import MessageIDGenerator
from chat_service.domain.chat.values.message_id import MessageID


class UUID4MessageIDGenerator(MessageIDGenerator):
    @override
    def __call__(self) -> MessageID:
        return cast(MessageID, uuid4())
