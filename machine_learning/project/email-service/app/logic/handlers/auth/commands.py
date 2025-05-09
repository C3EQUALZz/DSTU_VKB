from app.domain.entities.user import UserEntity
from app.domain.values.mail import Email
from app.domain.values.user import UserName, UserSurname, UserURL
from app.infrastructure.scheduler.tasks.schemas import UserSendEmailForVerificationJobSchema
from app.logic.commands.auth import SendVerificationEmailCommand
from app.logic.handlers.auth.base import AuthCommandHandler


class SendEmailVerificationToUser(
    AuthCommandHandler[SendVerificationEmailCommand],
):
    async def __call__(self, command: SendVerificationEmailCommand) -> None:
        user: UserEntity = UserEntity(
            name=UserName(command.name),
            surname=UserSurname(command.surname),
            email=Email(command.email),
            url=UserURL(command.url),
        )

        await self._scheduler.schedule_task(
            self.__class__,
            UserSendEmailForVerificationJobSchema.from_(user)
        )