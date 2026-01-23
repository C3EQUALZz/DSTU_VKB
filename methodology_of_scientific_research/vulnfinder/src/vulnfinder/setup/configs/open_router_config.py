from pydantic import BaseModel, Field


class OpenRouterConfig(BaseModel):
    url: str = Field(
        default="https://openrouter.ai/api/v1",
        description="The URL to the OpenRouter API",
        alias="OPENROUTER_URL",
    )
    api_key: str = Field(description="The OpenRouter API key", alias="OPENROUTER_API_KEY")
    default_model: str = Field(
        default="gpt-4o-mini",
        description="Default LLM model",
        alias="OPENROUTER_DEFAULT_MODEL",
    )
    embedding_model: str = Field(
        default="text-embedding-3-small",
        description="Embedding model name",
        alias="OPENROUTER_EMBEDDING_MODEL",
    )
