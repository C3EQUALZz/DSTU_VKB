import logging
from typing import Final, override

from app.domain.entities.user import UserEntity
from app.domain.values.user import UserName, UserSurname, UserEmail, UserPassword
from app.infrastructure.security.password import hash_password
from app.infrastructure.services.users import UsersService
from app.logic.commands.auth import UserRegisterCommand
from app.logic.events.auth import UserRegisterEvent
from app.logic.handlers.users.base import UsersCommandHandler

logger: Final[logging.Logger] = logging.getLogger(__file__)


class UserRegisterCommandHandler(UsersCommandHandler[UserRegisterCommand]):
    @override
    async def __call__(self, command: UserRegisterCommand) -> UserEntity:
        async with self._users_uow as uow:
            user_service: UsersService = UsersService(uow)

            new_user: UserEntity = UserEntity(
                name=UserName(command.name),
                surname=UserSurname(command.surname),
                email=UserEmail(command.email),
                password=UserPassword(hash_password(command.password)),
            )

            created_user: UserEntity = await user_service.add(new_user)

            logger.info("User (%s) registered successfully in auth service", created_user.email)

            self._event_buffer.add(
                UserRegisterEvent(
                    email=created_user.email.as_generic_type(),
                    name=created_user.name.as_generic_type(),
                    surname=created_user.surname.as_generic_type(),
                    role=created_user.role.as_generic_type(),
                )
            )

            return created_user
