from abc import ABC

from app.infrastructure.integrations.llm.message.text.base import LLMTextMessageProvider
from app.infrastructure.uow.base import AbstractUnitOfWork


class MessagesUnitOfWork(AbstractUnitOfWork, ABC):
    """
    An interface for work with messages from user, that is used by service layer of messages module.
    The main goal is that implementations of this interface can be easily replaced in the service layer
    using dependency injection without disrupting its functionality.
    """
    text: LLMTextMessageProvider
