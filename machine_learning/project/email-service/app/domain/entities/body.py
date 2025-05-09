from dataclasses import dataclass
from typing import Any

from app.domain.entities.base import BaseEntity
from app.domain.values.body import EmailBodyTitle


@dataclass(eq=False)
class BodyOfEmailEntity(BaseEntity):
    title: EmailBodyTitle
    template_context: dict[str, Any]
