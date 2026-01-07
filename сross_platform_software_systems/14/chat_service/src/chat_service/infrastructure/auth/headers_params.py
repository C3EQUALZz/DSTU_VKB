from typing import Annotated

from fastapi import Header
from pydantic import BaseModel


class HeaderParams(BaseModel):
    x_user_id: str


header_params = Annotated[HeaderParams, Header()]
