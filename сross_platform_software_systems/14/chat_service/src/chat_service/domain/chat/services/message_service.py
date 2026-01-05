import logging
from datetime import datetime, UTC
from typing import Final

from chat_service.domain.chat.entities import Message
from chat_service.domain.chat.events import (
    MessageCreatedEvent,
    MessageContentChangedEvent,
    MessageRoleChangedEvent,
    MessageSuccessfullySentEvent, MessageFailedSentEvent
)
from chat_service.domain.chat.ports.message_id_generator import MessageIDGenerator
from chat_service.domain.chat.values.message_content import MessageContent
from chat_service.domain.chat.values.message_role import MessageRole
from chat_service.domain.chat.values.message_status import MessageStatus
from chat_service.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class MessageService(DomainService):
    def __init__(
            self,
            message_id_generator: MessageIDGenerator,
    ) -> None:
        super().__init__()
        self._message_id_generator: Final[MessageIDGenerator] = message_id_generator

    def create(
            self,
            content: MessageContent,
            role: MessageRole | None = None,
    ) -> Message:
        logger.debug(
            "Started creating message with content: %s and role: %s in message service",
            content,
            role
        )

        message_role: MessageRole = (
            MessageRole.USER if role is None else role
        )

        new_message: Message = Message(
            id=self._message_id_generator(),
            content=content,
            role=message_role,
        )

        logger.debug("Created new instance of message: %s", new_message)

        new_event: MessageCreatedEvent = MessageCreatedEvent(
            message_id=new_message.id,
            message_content=new_message.content.value,
            sender_role=new_message.role
        )

        self._record_event(new_event)

        logger.debug("Created new event for message: %s", new_event)

        return new_message

    def change_message_content(
            self,
            message: Message,
            new_content: MessageContent
    ) -> None:
        logger.debug(
            "Started changing message content for message: %s, new content: %s",
            message,
            new_content
        )

        message.content = new_content
        message.updated_at = datetime.now(UTC)

        new_event: MessageContentChangedEvent = MessageContentChangedEvent(
            message_id=message.id,
            message_content=message.content.value,
        )

        self._record_event(new_event)

        logger.debug("Created new event for message: %s", new_event)

    def change_message_role(
            self,
            message: Message,
            new_role: MessageRole
    ) -> None:
        logger.debug(
            "Started changing message %s for new role: %s",
            message,
            new_role
        )

        message.role = new_role
        message.updated_at = datetime.now(UTC)

        new_event: MessageRoleChangedEvent = MessageRoleChangedEvent(
            message_id=message.id,
            sender_role=message.role,
        )

        self._record_event(new_event)

        logger.debug(
            "Created new event for message: %s",
            new_event
        )

    def mark_message_as_successfully_sent(
            self,
            message: Message
    ) -> None:
        """
        Mark the message as successfully sent.
        :param message: message to mark as success.
        :return: None
        """
        logger.debug(
            "Started marking message as successfully sent: %s",
            message
        )

        message.status = MessageStatus.SENT
        message.updated_at = datetime.now(UTC)

        new_event: MessageSuccessfullySentEvent = MessageSuccessfullySentEvent(
            message_id=message.id,
        )

        self._record_event(new_event)

        logger.debug(
            "Created new event for message: %s",
            new_event
        )

    def mark_message_as_failed(
            self,
            message: Message
    ) -> None:
        """
        Mark the message as failed. Produces new event for event bus
        :param message: message to mark as failed.
        :return: None
        """
        message.status = MessageStatus.FAILED
        message.updated_at = datetime.now(UTC)

        new_event: MessageFailedSentEvent = MessageFailedSentEvent(
            message_id=message.id,
        )

        self._record_event(new_event)

        logger.debug(
            "Created new event for message: %s",
            new_event
        )
