"""Formatter for converting Chat domain entities to OpenRouter API format."""
from collections import deque
from typing import Iterable

from openai.types.chat import (
    ChatCompletionAssistantMessageParam,
    ChatCompletionChunk,
    ChatCompletionSystemMessageParam,
    ChatCompletionUserMessageParam,
    ChatCompletionMessageParam,
)

from chat_service.application.common.ports.chat.openrouter_gateway import StreamChunkDTO
from chat_service.domain.chat.entities import Chat
from chat_service.domain.chat.values.message_role import MessageRole


class ChatMessageFormatter:
    """Formats chat messages for OpenRouter API."""

    @staticmethod
    def format_messages(chat: Chat) -> Iterable[ChatCompletionMessageParam]:
        """Format chat messages for OpenRouter API.

        Args:
            chat: The chat entity to format.

        Returns:
            List of typed message parameters for OpenAI SDK.
        """
        formatted_messages: deque[ChatCompletionMessageParam] = deque()

        for message in chat.get_messages():
            content = str(message.content.value)

            if message.role == MessageRole.USER:
                formatted_messages.append(
                    ChatCompletionUserMessageParam(
                        role="user",
                        content=content,
                    )
                )
            elif message.role == MessageRole.ASSISTANT:
                formatted_messages.append(
                    ChatCompletionAssistantMessageParam(
                        role="assistant",
                        content=content,
                    )
                )
            elif message.role == MessageRole.SYSTEM:
                formatted_messages.append(
                    ChatCompletionSystemMessageParam(
                        role="system",
                        content=content,
                    )
                )

        return formatted_messages

    @staticmethod
    def convert_chunk_to_dto(
            chunk: ChatCompletionChunk,
            model: str,
    ) -> StreamChunkDTO:
        """Convert OpenAI chunk to StreamChunkDTO.

        Args:
            chunk: The chunk from OpenAI SDK.
            model: The model name.

        Returns:
            StreamChunkDTO instance.
        """
        delta = chunk.choices[0].delta
        content = delta.content or ""
        finish_reason = chunk.choices[0].finish_reason
        is_finished = finish_reason is not None

        return StreamChunkDTO(
            content=content,
            is_finished=is_finished,
            finish_reason=finish_reason,
            model=chunk.model or model,
        )
