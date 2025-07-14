from typing import Protocol, Iterable
from abc import abstractmethod
from cryptography_methods.domain.user.values.user_id import UserID


class ViewManager(Protocol):
    @abstractmethod
    async def send_message_to_user(
            self,
            user_id: UserID,
            message: str
    ) -> None:
        ...

    @abstractmethod
    async def send_table_to_user(
            self,
            user_id: UserID,
            table: Iterable[Iterable[str]],
            headers: Iterable[str] | None = None,
    ) -> None:
        ...

    @abstractmethod
    async def send_greeting_to_user(
            self,
            user_id: UserID,
    ) -> None:
        ...
