import os

from openai import AsyncOpenAI


async def get_openrouter_client() -> AsyncOpenAI:
    return AsyncOpenAI(
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://api.proxyapi.ru/openrouter/v1",
    )
