from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserNotFoundException
from app.infrastructure.services.users import UsersService

from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
    UpdateUserCommand,
)

from app.logic.events.users import UserCreateEvent, UserDeleteEvent, UserUpdateEvent
from app.logic.handlers.users.base import UsersCommandHandler


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> UserEntity:
        """
        Handler for creating a new user.
        """
        async with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            new_user: UserEntity = UserEntity(first_name=command.first_name)

            added_user: UserEntity = await user_service.add(new_user)

            await uow.add_event(
                UserCreateEvent(
                    oid=added_user.oid,
                    first_name=added_user.first_name,
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

            if not await user_service.check_existence(oid=command.oid):
                raise UserNotFoundException(command.oid)

            user: UserEntity = await user_service.get_by_id(command.oid)

            updated_user = UserEntity(**await command.to_dict())
            updated_user.oid = user.oid

            updated_user: UserEntity = await user_service.update(updated_user)

            await uow.add_event(
                UserUpdateEvent(
                    oid=updated_user.oid,
                    first_name=updated_user.first_name,
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

            await uow.add_event(
                UserDeleteEvent(
                    user_oid=command.oid,
                )
            )

            return deleted_user
