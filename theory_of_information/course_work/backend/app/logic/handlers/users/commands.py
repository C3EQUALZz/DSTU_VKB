from app.domain.entities.user import UserEntity
from app.domain.values.user import Password
from app.exceptions.infrastructure import UserNotFoundException
from app.exceptions.logic import UserAlreadyExistsException
from app.infrastructure.services.users import UsersService
from app.infrastructure.utils.security import hash_password
from app.logic.commands.users import CreateUserCommand, UpdateUserCommand, DeleteUserCommand
from app.logic.events.users import UserDeleteEvent
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

        if not await user_service.check_existence(oid=command.oid):
            raise UserNotFoundException(command.oid)

        user: UserEntity = await user_service.get_by_id(command.oid)

        updated_user = UserEntity(**await command.to_dict())
        updated_user.oid = user.oid
        updated_user.password = Password(hash_password(command.password))

        return await user_service.update(updated_user)


class DeleteUserCommandHandler(UsersCommandHandler[DeleteUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> None:
        async with self._uow as uow:
            user_service: UsersService = UsersService(uow=uow)

            if not await user_service.check_existence(oid=command.oid):
                raise UserNotFoundException(command.oid)

            deleted_user = await user_service.delete(oid=command.oid)

            await uow.add_event(
                UserDeleteEvent(
                    user_oid=command.oid,
                )
            )

            return deleted_user
