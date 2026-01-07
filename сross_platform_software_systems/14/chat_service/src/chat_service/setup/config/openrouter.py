from pydantic import BaseModel, Field


class OpenRouterConfig(BaseModel):
    api_key: str = Field(alias="OPENROUTER_API_KEY", description="API Key")
    base_url: str = "https://api.proxyapi.ru/openrouter/v1"