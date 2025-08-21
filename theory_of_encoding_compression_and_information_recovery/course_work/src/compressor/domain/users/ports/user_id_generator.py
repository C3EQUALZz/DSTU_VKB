from abc import abstractmethod
from typing import Protocol

from compressor.domain.users.values.user_id import UserID


class UserIDGenerator(Protocol):
    @abstractmethod
    def __call__(self) -> UserID: ...
