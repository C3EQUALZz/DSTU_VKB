from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True, slots=True)
class CurrentUser:
    id: int
    username: str


class AccountAlreadyExists(ValueError):
    pass


class IdentityStore(Protocol):
    def register(
        self, username: str, email: str, password: str, previous_session_id: str | None
    ) -> str: ...

    def login(
        self, username: str, password: str, previous_session_id: str | None
    ) -> str | None: ...

    def resolve(self, session_id: str | None) -> CurrentUser | None: ...

    def revoke(self, session_id: str) -> None: ...
