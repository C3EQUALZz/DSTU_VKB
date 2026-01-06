from collections.abc import AsyncIterator
from dataclasses import dataclass
from typing import Protocol
from abc import abstractmethod
from chat_service.domain.chat.entities import Chat


@dataclass(frozen=True, slots=True, kw_only=True)
class StreamChunkDTO:
    """DTO representing a chunk of streamed response from OpenRouter.

    Attributes:
        content: The text content of this chunk.
        is_finished: Whether the stream has finished.
        finish_reason: Reason for completion (e.g., "stop", "length", "content_filter").
        model: The model that generated this response.
        usage_tokens: Number of tokens used (if available).
    """

    content: str
    is_finished: bool = False
    finish_reason: str | None = None
    model: str | None = None
    usage_tokens: int | None = None


@dataclass(frozen=True, slots=True, kw_only=True)
class ChatCompletionDTO:
    """DTO representing a complete non-streaming response from OpenRouter.

    Attributes:
        content: The full response content.
        model: The model that generated the response.
        finish_reason: Reason for completion.
        usage_tokens: Number of tokens used.
    """

    content: str
    model: str
    finish_reason: str | None = None
    usage_tokens: int | None = None


class OpenRouterGateway(Protocol):
    """Gateway for interacting with OpenRouter API."""

    @abstractmethod
    async def send_message_to_chat_streaming(
            self,
            chat: Chat,
    ) -> AsyncIterator[StreamChunkDTO]:
        """Send messages from chat to OpenRouter and stream the response.

        Args:
            chat: The chat entity containing messages and selected LLM.

        Yields:
            StreamChunkDTO: Chunks of the streaming response.

        Raises:
            ValueError: If user doesn't have an API key configured.
            RuntimeError: If API request fails.
        """
        ...

    @abstractmethod
    async def send_message_to_chat(
            self,
            chat: Chat,
    ) -> ChatCompletionDTO:
        """Send messages from chat to OpenRouter and get complete response.

        Args:
            chat: The chat entity containing messages and selected LLM.

        Returns:
            ChatCompletionDTO: Complete response from OpenRouter.

        Raises:
            ValueError: If user doesn't have an API key configured.
            RuntimeError: If API request fails.
        """
        ...
