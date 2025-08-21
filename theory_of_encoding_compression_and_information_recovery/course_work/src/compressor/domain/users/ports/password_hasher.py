from abc import abstractmethod
from typing import Protocol

from compressor.domain.users.values.user_password_hash import UserPasswordHash
from compressor.domain.users.values.user_raw_password import UserRawPassword


class PasswordHasher(Protocol):
    @abstractmethod
    def hash(self, raw_password: UserRawPassword) -> UserPasswordHash: ...

    @abstractmethod
    def verify(self, *, raw_password: UserRawPassword, hashed_password: UserPasswordHash) -> bool: ...
