import logging
from typing import Final

from dishka import FromDishka
from dishka.integrations.taskiq import inject

from app.domain.entities.body import BodyOfEmailEntity
from app.domain.entities.mail import EmailEntity
from app.domain.values.body import EmailBodyTitle
from app.domain.values.mail import Email, EmailSubject, TemplateName
from app.infrastructure.scheduler import scheduler
from app.infrastructure.scheduler.tasks.schemas import UserSendEmailForVerificationJobSchema
from app.infrastructure.services.mail.base import BaseMailSender
from app.settings.configs.enums import TaskNamesConfig

logger: Final[logging.Logger] = logging.getLogger(__name__)


@scheduler.task(task_name=TaskNamesConfig.SEND_VERIFICATION_EMAIL)
@inject(patch_module=True)
async def send_verification_email(
        schemas: UserSendEmailForVerificationJobSchema,
        service: FromDishka[BaseMailSender]
) -> None:
    logger.info(
        "Started sending verification email for user with name %s and surname %s",
        schemas.name,
        schemas.surname
    )

    email_entity: EmailEntity = EmailEntity(
        recipients=[Email(str(schemas.email))],
        subject=EmailSubject("'Pomogator' verification email for user"),
        body=BodyOfEmailEntity(
            title=EmailBodyTitle("Account verification email"),
            template_context={
                "name": schemas.name,
                "surname": schemas.surname,
                "url": str(schemas.url)
            }
        ),
        template_name=TemplateName("verification_email.html"),
    )

    await service.send_message(email_entity=email_entity)

    logger.info("Sent email to user successfully")
