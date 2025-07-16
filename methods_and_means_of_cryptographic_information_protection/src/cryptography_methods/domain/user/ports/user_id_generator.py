from abc import abstractmethod
from typing import Protocol

from cryptography_methods.domain.user.values.user_id import UserID


class UserIdGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> UserID:
        ...
