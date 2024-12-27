from app.domain.entities.user import UserEntity
from app.infrastructure.exceptions import UserNotFoundException
from app.infrastructure.security.utils.coders import validate_password
from app.infrastructure.services.users import UsersService
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.exceptions import InvalidPasswordException
from app.logic.handlers.auth.base import AuthCommandHandler


class VerifyUserCredentialsCommandHandler(AuthCommandHandler[VerifyUserCredentialsCommand]):
    async def __call__(self, command: VerifyUserCredentialsCommand) -> UserEntity:
        """
        Checks, if provided by user credentials are valid.
        """

        users_service: UsersService = UsersService(uow=self._uow)

        user: UserEntity
        if await users_service.check_existence(email=command.name):
            user = await users_service.get_by_email(email=command.name)
        elif await users_service.check_existence(name=command.name):
            user = await users_service.get_by_name(name=command.name)
        else:
            raise UserNotFoundException(command.name)

        if not validate_password(password=command.password, hashed_password=user.password.as_generic_type()):
            raise InvalidPasswordException

        return user
