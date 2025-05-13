from app.domain.entities.user import UserEntity
from app.domain.values.user import Role, Password, Email
from app.exceptions.infrastructure import UserNotFoundException
from app.infrastructure.services.users import UsersService
from app.infrastructure.utils.security import hash_password

from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
)

from app.logic.events.users import UserCreatedEvent, UserDeletedEvent, UserUpdatedEvent
from app.logic.handlers.users.base import UsersCommandHandler


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> UserEntity:
        """
        Handler for creating a new user.
        """
        async with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            new_user: UserEntity = UserEntity(
                name=command.name,
                surname=command.surname,
                email=Email(command.email),
                password=Password(hash_password(command.password)),
                telegram_id=command.telegram_id,
                role=Role(command.role),
            )

            added_user: UserEntity = await user_service.add(new_user)

            self._event_buffer.add(
                UserCreatedEvent(
                    oid=added_user.oid,
                    first_name=added_user.name,
                    role=added_user.role.as_generic_type(),
                )
            )

            return added_user


class UpdateUserCommandHandler(UsersCommandHandler[UpdateUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> UserEntity:
        """
        Updates a user, if user with provided credentials exist, and updates event signaling that
        operation was successfully executed. In other case raises BookNotExistsException.
        :param command: command to execute which must be linked in app/logic/handlers/__init__
        :return: domain entity of the updated book
        """
        async with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            if not await user_service.check_existence(oid=command.user_id):
                raise UserNotFoundException(command.user_id)

            user: UserEntity = await user_service.get_by_id(command.user_id)

            user_info_from_command = await command.to_dict(exclude={"oid"})
            user_info_from_command["oid"] = user_info_from_command.pop("user_id")
            user.set_attrs(user_info_from_command)

            updated_user: UserEntity = await user_service.update(user)

            self._event_buffer.add(
                UserUpdatedEvent(
                    oid=updated_user.oid,
                    first_name=updated_user.name,
                    role=updated_user.role.as_generic_type(),
                )
            )

            return updated_user


class DeleteUserCommandHandler(UsersCommandHandler[DeleteUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> None:
        async with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            if not await user_service.check_existence(oid=command.oid):
                raise UserNotFoundException(f"Couldn't find user {command.oid}")

            deleted_user: None = await user_service.delete(oid=command.oid)

            self._event_buffer.add(
                UserDeletedEvent(
                    user_oid=command.oid,
                )
            )

            return deleted_user
