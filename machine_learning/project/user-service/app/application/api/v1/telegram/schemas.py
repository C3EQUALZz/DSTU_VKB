from typing import Self, cast

from pydantic import BaseModel, AnyHttpUrl, Field


class DeepLinkTelegramResponse(BaseModel):
    url: AnyHttpUrl = Field(..., description="Pydantic field for telegram url link")

    @classmethod
    def from_(cls, url: str) -> Self:
        return cls(url=cast(AnyHttpUrl, url))
