from pydantic import BaseModel, Field


class OpenRouterConfig(BaseModel):
    url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="The URL to the OpenRouter API",
        alias="OPENROUTER_URL"
    )
    api_key: str = Field(
        description="The OpenRouter API key",
        alias="OPENROUTER_API_KEY"
    )
    default_model: str = Field(

    )
