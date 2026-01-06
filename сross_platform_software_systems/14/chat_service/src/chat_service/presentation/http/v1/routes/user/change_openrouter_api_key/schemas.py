from typing import Annotated

from pydantic import BaseModel, Field


class ChangeOpenRouterAPIRequestSchema(BaseModel):
    new_openrouter_api_key: Annotated[
        str,
        Field(
            min_length=1,
            max_length=100,
            description="The new openrouter API key",
            examples=["sk-sdfgsjh11231nfwhjef-ajfjNF-QNJQNWF1-12J1N2KF"]
        )
    ]

