from app.domain.entities.user import UserEntity
from app.exceptions.infrastructure import UserNotFoundError
from app.exceptions.logic import UserAlreadyExistsError
from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand,
)
from app.logic.handlers.users.base import UsersCommandHandler


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> UserEntity:
        """
        Handler for creating a new user.
        """

        if await self._user_service.check_existence(command.user_id):
            raise UserAlreadyExistsError(command.user_id)

        new_user: UserEntity = UserEntity(**await command.to_dict())

        added_user: UserEntity = await self._user_service.add(new_user)

        return added_user


class DeleteUserCommandHandler(UsersCommandHandler[DeleteUserCommand]):
    async def __call__(self, command: DeleteUserCommand) -> None:
        if not await self._user_service.check_existence(oid=command.user_id):
            raise UserNotFoundError(command.user_id)

        deleted_user: None = await self._user_service.delete(oid=command.user_id)

        return deleted_user
