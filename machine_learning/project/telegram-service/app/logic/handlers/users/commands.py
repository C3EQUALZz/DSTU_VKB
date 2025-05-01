from app.logic.commands.users import (
    CreateUserCommand,
    DeleteUserCommand, UpdateUserCommand,
)
from app.logic.events.user import UserCreateEvent, UserDeleteEvent, UserUpdateEvent
from app.logic.handlers.users.base import UsersCommandHandler


class CreateUserCommandHandler(UsersCommandHandler[CreateUserCommand]):
    async def __call__(self, command: CreateUserCommand) -> None:
        """
        Handler for creating a new user.
        """
        self._event_buffer.add(
            UserCreateEvent(
                user_id=command.user_id,
                full_name=command.full_name,
                role=command.role,
                language_code=command.language_code,
                user_login=command.user_login,
            )
        )


class DeleteUserCommandHandler(UsersCommandHandler[DeleteUserCommand]):
    async def __call__(self, command: DeleteUserCommand) -> None:
        """
        Handler for deleting a user.
        """
        self._event_buffer.add(
            UserDeleteEvent(
                user_id=command.user_id,
            )
        )


class UserUpdateCommandHandler(UsersCommandHandler[UpdateUserCommand]):
    async def __call__(self, command: UpdateUserCommand) -> None:
        self._event_buffer.add(
            UserUpdateEvent(
                user_id=command.user_id,
                full_name=command.full_name,
                language_code=command.language_code,
                role=command.role,
                user_login=command.user_login,
            )
        )
