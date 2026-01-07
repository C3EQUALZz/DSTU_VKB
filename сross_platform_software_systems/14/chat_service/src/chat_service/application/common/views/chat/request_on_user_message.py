from dataclasses import dataclass
from uuid import UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class RequestOnUserMessageView:
    user_message_id: UUID
    assistant_message_id: UUID
    assistant_message_content: str
