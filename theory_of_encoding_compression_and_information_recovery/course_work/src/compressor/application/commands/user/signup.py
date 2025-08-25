import logging
from dataclasses import dataclass
from typing import Final, final

from compressor.application.common.ports.transaction_manager import TransactionManager
from compressor.application.common.ports.user_command_gateway import UserCommandGateway
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.application.common.views.users import SignUpView
from compressor.application.errors.user import UserAlreadyExistsError
from compressor.domain.users.entities.user import User
from compressor.domain.users.services.user_service import UserService
from compressor.domain.users.values.user_raw_password import UserRawPassword
from compressor.domain.users.values.username import Username

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class SignUpCommand:
    username: str
    password: str


@final
class SignUpCommandHandler:
    def __init__(
            self,
            telegram_command_gateway: UserCommandGateway,
            telegram_query_gateway: UserQueryGateway,
            transaction_manager: TransactionManager,
            user_service: UserService,
    ) -> None:
        self._user_command_gateway: Final[UserCommandGateway] = telegram_command_gateway
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._user_service: Final[UserService] = user_service
        self._user_query_gateway: Final[UserQueryGateway] = telegram_query_gateway

    async def __call__(self, data: SignUpCommand) -> SignUpView:
        logger.info("Started registration with username: %s", data.username)

        if await self._user_command_gateway.read_by_username(
                username=Username(data.username),
        ):
            msg: str = "User with username {} not found".format(data.username)
            raise UserAlreadyExistsError(msg)

        logger.info("User not found in database, creating new user")

        new_user: User = self._user_service.create(
            username=Username(data.username),
            raw_password=UserRawPassword(data.password),
        )

        await self._user_command_gateway.add(user=new_user)
        await self._transaction_manager.flush()
        await self._transaction_manager.commit()

        logger.info("User was successfully registered with id: %d", new_user.id)

        return SignUpView(
            user_id=new_user.id,
        )
