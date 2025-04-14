from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    TypeVar,
    override,
)

from openai import AsyncOpenAI

from app.domain.entities.message import TextMessageEntity
from app.domain.values.message import Text
from app.infrastructure.integrations.llm.message.text.base import LLMTextMessageModel

if TYPE_CHECKING:
    from openai.types.chat import ChatCompletion

T = TypeVar(
    "T",
    "o3-mini",  # noqa
    "o1",  # noqa
    "o1-preview",  # noqa
    "o1-mini",  # noqa
    "gpt-4o",  # noqa
    "chatgpt-4o-latest",  # noqa
    "gpt-4o-mini",  # noqa
    "gpt-4-turbo",  # noqa
    "gpt-4",  # noqa
    "gpt-3.5-turbo",  # noqa
    "deepseek/deepseek-chat",  # noqa
)


class OpenAITextMessageModel(LLMTextMessageModel, Generic[T]):
    def __init__(self, client: AsyncOpenAI, model: T) -> None:
        self._client: AsyncOpenAI = client
        self._model: T = model

    @override
    async def send_message(
        self, message: TextMessageEntity, temperature: float = 0.7, max_tokens: int = 450
    ) -> TextMessageEntity | None:
        message: list[dict[str, Any]] = [await message.to_dict(exclude={"oid", "created_at", "updated_at"})]

        response: ChatCompletion = await self._client.chat.completions.create(
            model=self._model, messages=message, temperature=temperature, max_tokens=max_tokens
        )

        if content := response.choices[0].message.content:
            return TextMessageEntity(
                content=Text(content),
                role=response.choices[0].message.role,
            )
