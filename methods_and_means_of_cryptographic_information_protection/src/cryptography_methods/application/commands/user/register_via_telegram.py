from dataclasses import dataclass
from itertools import chain
from typing import final, Final, Iterable

from cryptography_methods.application.common.ports.user.command_gateway import UserCommandGateway
from cryptography_methods.application.common.transaction_manager import TransactionManager
from cryptography_methods.application.errors.user import UserAlreadyExists
from cryptography_methods.domain.common.events import BaseDomainEvent
from cryptography_methods.domain.user.entities.telegram import TelegramAccount
from cryptography_methods.domain.user.entities.user import User
from cryptography_methods.domain.user.services.telegram_service import TelegramService
from cryptography_methods.domain.user.services.user_service import UserService
from cryptography_methods.domain.user.values.first_name import FirstName
from cryptography_methods.domain.user.values.middle_name import MiddleName
from cryptography_methods.domain.user.values.second_name import SecondName
from cryptography_methods.domain.user.values.telegram_id import TelegramID
from cryptography_methods.domain.user.values.user_id import UserID
from cryptography_methods.infrastructure.event_bus.base import EventBus


@dataclass(frozen=True, slots=True)
class RegisterUserViaTelegramCommand:
    first_name: str
    telegram_id: int
    is_bot: bool
    second_name: str | None = None
    middle_name: str | None = None
    phone_number: str | None = None


@final
class RegisterUserViaTelegramCommandHandler:
    def __init__(
            self,
            user_gateway: UserCommandGateway,
            user_service: UserService,
            telegram_service: TelegramService,
            event_bus: EventBus,
            transaction_manager: TransactionManager,
    ) -> None:
        self._user_gateway: Final[UserCommandGateway] = user_gateway
        self._user_service: Final[UserService] = user_service
        self._event_bus: Final[EventBus] = event_bus
        self._transaction_manager: Final[TransactionManager] = transaction_manager
        self._telegram_service: Final[TelegramService] = telegram_service

    async def __call__(self, data: RegisterUserViaTelegramCommand) -> UserID:
        if self._user_gateway.read_by_telegram_id(TelegramID(data.telegram_id)):
            raise UserAlreadyExists("This user is already registered in application")

        new_user: User = self._user_service.create(
            first_name=FirstName(data.first_name),
            second_name=SecondName(data.second_name) if data.second_name else None,
            middle_name=MiddleName(data.middle_name) if data.middle_name else None,
        )

        telegram_account: TelegramAccount = self._telegram_service.create(
            id=TelegramID(data.telegram_id),
            is_bot=data.is_bot,
        )

        new_user.telegram_account = telegram_account

        await self._user_gateway.add(user=new_user)
        await self._transaction_manager.flush()

        events_for_publishing: Iterable[BaseDomainEvent] = chain(
            self._user_service.pull_events(),
            self._user_service.pull_events()
        )

        await self._event_bus.publish(events_for_publishing)
        await self._transaction_manager.commit()

        return new_user.id
