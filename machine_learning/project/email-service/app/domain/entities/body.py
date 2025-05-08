from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.body import EmailBodyTitle, EmailBodyMessage


@dataclass(eq=False)
class BodyOfEmailEntity(BaseEntity):
    title: EmailBodyTitle
    message: EmailBodyMessage
