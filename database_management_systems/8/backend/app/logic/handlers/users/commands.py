from typing import List

from app.domain.entities.user import UserEntity
from app.domain.values.users import Password
from app.infrastructure.security.utils.coders import (
    hash_password,
)
from app.infrastructure.services.users import UsersService
from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    GetAllUsersCommand,
    GetUserByIdCommand,
    UpdateUserCommand,
)
from app.logic.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from app.logic.handlers.users.base import UsersCommandHandler


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> UserEntity:
        """
        Handler for creating a new user.
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if await user_service.check_existence(name=command.name, email=command.email):
            raise UserAlreadyExistsException(command.email)

        new_user: UserEntity = UserEntity(**await command.to_dict())
        new_user.password = Password(hash_password(command.password))

        return await user_service.add(new_user)


class UpdateUserCommandHandler(UsersCommandHandler[UpdateUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> UserEntity:
        """
        Updates a user, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the updated book
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if await user_service.check_existence(oid=command.oid):
            raise UserAlreadyExistsException(command.oid)

        user: UserEntity = await user_service.get_by_id(command.oid)

        updated_user = UserEntity(**await command.to_dict())
        updated_user.oid = user.oid

        return await user_service.update(updated_user)


class DeleteUserCommandHandler(UsersCommandHandler[DeleteUserCommand]):
    async def __call__(self, command: DeleteUserCommand) -> None:
        """
        Deletes a user, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises UserNotFoundException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: None
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if not user_service.check_existence(oid=command.oid):
            raise UserNotFoundException(str(command.oid))

        await user_service.delete(oid=command.oid)


class GetAllUsersCommandHandler(UsersCommandHandler[GetAllUsersCommand]):
    async def __call__(self, command: GetAllUsersCommand) -> List[UserEntity]:
        """
        Get all users and signaling that operation was successfully executed.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the list of users
        """
        user_service: UsersService = UsersService(uow=self._uow)

        return await user_service.get_all()


class GetUserByIdCommandHandler(UsersCommandHandler[GetUserByIdCommand]):
    async def __call__(self, command: GetUserByIdCommand) -> UserEntity:
        """
        Gets user by id, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises UserNotFoundException.
        param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the user by id
        """
        user_service: UsersService = UsersService(uow=self._uow)

        if not await user_service.check_existence(oid=command.oid):
            raise UserNotFoundException(str(command.oid))

        return await user_service.get_by_id(oid=command.oid)
