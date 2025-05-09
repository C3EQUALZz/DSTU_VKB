from dataclasses import dataclass
from typing import Any

from app.domain.entities.base import BaseEntity
from app.domain.entities.body import BodyOfEmailEntity
from app.domain.values.mail import Email, TemplateName, EmailSubject


@dataclass(eq=False)
class EmailEntity(BaseEntity):
    recipients: list[Email]
    subject: EmailSubject
    body: BodyOfEmailEntity
    template_name: TemplateName
