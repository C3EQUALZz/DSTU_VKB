from app.domain.entities.user import UserEntity
from app.domain.values.user import Role, Password, Email
from app.exceptions.infrastructure import UserNotFoundError
from app.infrastructure.services.users import UsersService
from app.infrastructure.utils.security import hash_password

from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
)

from app.logic.handlers.users.base import UsersCommandHandler


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> UserEntity:
        """
        Handler for creating a new user.
        """
        with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            new_user: UserEntity = UserEntity(
                name=command.name,
                surname=command.surname,
                email=Email(command.email),
                password=Password(hash_password(command.password)),
                role=Role(command.role),
            )

            added_user: UserEntity = user_service.add(new_user)

            return added_user


class UpdateUserCommandHandler(UsersCommandHandler[UpdateUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> UserEntity:
        """
        Updates a user, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the updated book
        """
        with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            if not user_service.check_existence(oid=command.user_id):
                raise UserNotFoundError(command.user_id)

            user: UserEntity = user_service.get_by_id(command.user_id)

            user_info_from_command = await command.to_dict(exclude={"oid"})
            user_info_from_command["oid"] = user_info_from_command.pop("user_id")
            user.set_attrs(user_info_from_command)

            updated_user: UserEntity = user_service.update(user)

            return updated_user


class DeleteUserCommandHandler(UsersCommandHandler[DeleteUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> None:
        with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            if not user_service.check_existence(oid=command.user_id):
                raise UserNotFoundError(f"Couldn't find user {command.user_id}")

            return user_service.delete(oid=command.user_id)
