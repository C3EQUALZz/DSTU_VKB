from typing import TypeVar, Generic, Any, override

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletion

from app.domain.entities.message import MessageEntity
from app.domain.values.message import Text
from app.infrastructure.integrations.llm.dto.message import TextMessageDTO
from app.infrastructure.integrations.llm.message.base import BaseLLMProvider

T = TypeVar(
    "T",
    "o3-mini",
    "o3-mini-2025-01-31",
    "o1",
    "o1-2024-12-17",
    "o1-preview",
    "o1-preview-2024-09-12",
    "o1-mini",
    "o1-mini-2024-09-12",
    "gpt-4o",
    "gpt-4o-2024-11-20",
    "gpt-4o-2024-08-06",
    "gpt-4o-2024-05-13",
    "gpt-4o-audio-preview",
    "gpt-4o-audio-preview-2024-10-01",
    "gpt-4o-audio-preview-2024-12-17",
    "gpt-4o-mini-audio-preview",
    "gpt-4o-mini-audio-preview-2024-12-17",
    "gpt-4o-search-preview",
    "gpt-4o-mini-search-preview",
    "gpt-4o-search-preview-2025-03-11",
    "gpt-4o-mini-search-preview-2025-03-11",
    "chatgpt-4o-latest",
    "gpt-4o-mini",
    "gpt-4o-mini-2024-07-18",
    "gpt-4-turbo",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-0125-preview",
    "gpt-4-turbo-preview",
    "gpt-4-1106-preview",
    "gpt-4-vision-preview",
    "gpt-4",
    "gpt-4-0314",
    "gpt-4-0613",
    "gpt-4-32k",
    "gpt-4-32k-0314",
    "gpt-4-32k-0613",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
    "gpt-3.5-turbo-0301",
    "gpt-3.5-turbo-0613",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo-16k-0613"
)


class OpenAITextProvider(BaseLLMProvider, Generic[T]):
    def __init__(
            self,
            client: AsyncOpenAI,
            model: T
    ) -> None:
        self._client: AsyncOpenAI = client
        self._model: T = model

    @override
    async def send_message(self, dto: TextMessageDTO) -> MessageEntity | None:

        message: list[dict[str, Any]] = [await dto.message.to_dict(exclude={"oid"})]
        temperature: float = dto.temperature
        max_tokens: int = dto.max_tokens

        response: ChatCompletion = await self._client.chat.completions.create(
            model=self._model,
            messages=message,
            temperature=temperature,
            max_tokens=max_tokens
        )

        if content := response.choices[0].message.content:
            return MessageEntity(
                content=Text(content),
                role=response.choices[0].message.role,
            )
