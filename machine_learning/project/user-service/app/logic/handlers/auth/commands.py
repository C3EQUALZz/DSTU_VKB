from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserNotFoundException
from app.exceptions.logic import InvalidPasswordError
from app.infrastructure.services.users import UsersService
from app.infrastructure.utils.security import validate_password
from app.logic.commands.auth import VerifyUserCredentialsCommand
from app.logic.handlers.auth.base import AuthCommandHandler


class VerifyUserCredentialsCommandHandler(AuthCommandHandler[VerifyUserCredentialsCommand]):
    async def __call__(self, command: VerifyUserCredentialsCommand) -> UserEntity:
        """
        Checks, if provided by user credentials are valid.
        """
        users_service: UsersService = UsersService(uow=self._users_uow)

        user: UserEntity
        if await users_service.check_existence(email=command.email):
            user = await users_service.get_by_email(email=command.email)
        else:
            raise UserNotFoundException(command.email)

        if not validate_password(password=command.password, hashed_password=user.password.as_generic_type()):
            raise InvalidPasswordError(command.password)

        return user