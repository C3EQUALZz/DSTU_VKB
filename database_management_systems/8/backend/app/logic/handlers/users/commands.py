from app.domain.entities.user import UserEntity
from app.domain.values.users import Password
from app.infrastructure.exceptions import UserNotFoundError
from app.infrastructure.security.utils.coders import hash_password, validate_password
from app.infrastructure.services.users import UsersService
from app.logic.commands.users import CreateUserCommand, VerifyUserCredentialsCommand, UpdateUserCommand, \
    DeleteUserCommand
from app.logic.exceptions import UserAlreadyExistsException, InvalidPasswordException, UserNotFoundException
from app.logic.handlers.users.base import UsersCommandHandler


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> UserEntity:
        """
        Handler for creating a new user.
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if user_service.check_user_existence(email=command.email, name=command.name):
            raise UserAlreadyExistsException

        new_user: UserEntity = UserEntity(**await command.to_dict())
        new_user.password = Password(hash_password(command.password))

        new_user = await user_service.create_user(new_user)

        return new_user


class UpdateUserCommandHandler(UsersCommandHandler[UpdateUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> UserEntity:
        """
        Updates a user, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the updated book
        """
        ...


class DeleteUserCommandHandler(UsersCommandHandler[DeleteUserCommand]):
    async def __call__(self, command: DeleteUserCommand) -> None:
        """
        Deletes a user, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises UserNotFoundException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: None
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if not user_service.check_user_existence(oid=command.oid):
            raise UserNotFoundException(str(command.oid))

        await user_service.delete_user(oid=command.oid)


class VerifyUserCredentialsCommandHandler(UsersCommandHandler[VerifyUserCredentialsCommand]):
    async def __call__(self, command: VerifyUserCredentialsCommand) -> UserEntity:
        """
        Checks, if provided by user credentials are valid.
        """

        users_service: UsersService = UsersService(uow=self._uow)

        user: UserEntity
        if await users_service.check_user_existence(email=command.name):
            user = await users_service.get_user_by_email(email=command.name)
        elif await users_service.check_user_existence(name=command.name):
            user = await users_service.get_user_by_name(name=command.name)
        else:
            raise UserNotFoundError

        if not validate_password(password=command.password, hashed_password=user.password.as_generic_type()):
            raise InvalidPasswordException

        return user
