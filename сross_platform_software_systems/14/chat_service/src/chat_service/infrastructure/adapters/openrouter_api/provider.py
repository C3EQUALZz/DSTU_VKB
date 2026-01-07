from openai import AsyncOpenAI

from chat_service.setup.config.openrouter import OpenRouterConfig


async def get_openrouter_client(config: OpenRouterConfig) -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=config.api_key,
        base_url=config.base_url,
    )
