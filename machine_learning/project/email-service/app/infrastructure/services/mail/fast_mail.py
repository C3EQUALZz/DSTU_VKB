from typing import override, Final

from fastapi_mail import FastMail, MessageSchema, MessageType

from app.domain.entities.mail import EmailEntity
from app.infrastructure.services.mail.base import BaseMailSender
from app.infrastructure.services.mail.schemas import EmailSchema
from app.infrastructure.services.template_renderer.base import BaseTemplateRenderer


class FastMailSender(BaseMailSender):
    """
    Class for sending emails using FastMail library.
    """

    def __init__(self, fastmail_app: FastMail, renderer: BaseTemplateRenderer) -> None:
        """
        :param fastmail_app: FastMail instance for sending emails
        """
        self._fastmail: Final[FastMail] = fastmail_app
        self._renderer: Final[BaseTemplateRenderer] = renderer

    @override
    async def send_message(self, email_entity: EmailEntity) -> None:
        await self._fastmail.send_message(
            message=MessageSchema(
                recipients=[EmailSchema.from_(recipient).value for recipient in email_entity.recipients],
                subject=email_entity.subject.as_generic_type(),
                subtype=MessageType(email_entity.template_name.as_generic_type()),
                body=self._renderer.render(email_entity.template_name, email_entity.body)
            )
        )
