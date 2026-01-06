import logging
from collections.abc import AsyncIterator
from typing import Final, override, Iterable

from openai import AsyncOpenAI, AsyncStream
from openai.types.chat import ChatCompletionChunk, ChatCompletionMessageParam, ChatCompletion

from chat_service.application.common.ports.chat.openrouter_gateway import (
    OpenRouterGateway,
    ChatCompletionDTO,
    StreamChunkDTO
)
from chat_service.domain.chat.entities import Chat
from chat_service.infrastructure.adapters.openrouter_api.chat_message_formatter import (
    ChatMessageFormatter,
)
from chat_service.infrastructure.errors.openrouter import FailedToGetResponse

logger: Final[logging.Logger] = logging.getLogger(__name__)


class OpenAIOpenRouterGateway(OpenRouterGateway):
    """OpenAI-compatible gateway for OpenRouter API."""

    def __init__(
            self,
            open_router_client: AsyncOpenAI,
            message_formatter: ChatMessageFormatter,
    ) -> None:
        self._open_router_client: Final[AsyncOpenAI] = open_router_client
        self._message_formatter: Final[ChatMessageFormatter] = message_formatter

    @override
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
        messages: Iterable[ChatCompletionMessageParam] = self._message_formatter.format_messages(chat)
        model: str = chat.selected_llm.value

        logger.info(
            "Sending streaming request to OpenRouter: model=%s",
            model,
        )

        try:
            stream: AsyncStream[ChatCompletionChunk] = await self._open_router_client.chat.completions.create(
                model=model,
                messages=messages,
                stream=True,
                extra_headers={
                    "HTTP-Referer": "https://github.com/your-repo",
                    "X-Title": "Chat Service",
                },
            )

            async for chunk in stream:
                chunk_dto = self._message_formatter.convert_chunk_to_dto(chunk, model)
                yield chunk_dto

                if chunk_dto.is_finished:
                    logger.info(
                        "Stream finished: model=%s, finish_reason=%s",
                        model,
                        chunk_dto.finish_reason,
                    )
                    break

        except Exception as e:
            logger.exception(
                "Failed to stream response from OpenRouter: model=%s",
                model,
            )
            msg = f"OpenRouter API request failed: {e}"
            raise FailedToGetResponse(msg) from e

    @override
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
        messages: Iterable[ChatCompletionMessageParam] = self._message_formatter.format_messages(chat)
        model: str = chat.selected_llm.value

        logger.info(
            "Sending non-streaming request to OpenRouter: model=%s",
            model,
        )

        try:
            response: ChatCompletion = await self._open_router_client.chat.completions.create(
                model=model,
                messages=messages,
                stream=False,
                extra_headers={
                    "HTTP-Referer": "https://github.com/your-repo",
                    "X-Title": "Chat Service",
                },
            )

            content = response.choices[0].message.content or ""
            finish_reason = response.choices[0].finish_reason
            usage_tokens = response.usage.total_tokens if response.usage else None

            logger.info(
                "Received response from OpenRouter: model=%s, finish_reason=%s, tokens=%s",
                model,
                finish_reason,
                usage_tokens,
            )

            return ChatCompletionDTO(
                content=content,
                model=response.model,
                finish_reason=finish_reason,
                usage_tokens=usage_tokens,
            )

        except Exception as e:
            logger.exception(
                "Failed to get response from OpenRouter: model=%s",
                model
            )
            msg = f"OpenRouter API request failed: {e}"
            raise FailedToGetResponse(msg) from e
