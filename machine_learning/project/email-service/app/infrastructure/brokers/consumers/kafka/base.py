from typing import Annotated
from uuid import UUID

from pydantic import BeforeValidator, Field, PlainSerializer

StringUUID = Annotated[
    UUID,
    BeforeValidator(lambda x: UUID(x) if isinstance(x, str) else x),
    PlainSerializer(lambda x: str(x)),
    Field(
        description="Better annotation for UUID, parses from string format. Serializes to string format."
    ),
]
