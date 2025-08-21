from typing import Final

from compressor.domain.common.services.base import DomainService
from compressor.domain.users.entities.user import User
from compressor.domain.users.ports.password_hasher import PasswordHasher
from compressor.domain.users.ports.user_id_generator import UserIDGenerator
from compressor.domain.users.values.user_raw_password import UserRawPassword
from compressor.domain.users.values.user_role import UserRole
from compressor.domain.users.values.username import Username


class UserService(DomainService):
    def __init__(
            self,
            user_id_generator: UserIDGenerator,
            password_hasher: PasswordHasher,
    ) -> None:
        super().__init__()
        self._user_id_generator: Final[UserIDGenerator] = user_id_generator
        self._password_hasher: Final[PasswordHasher] = password_hasher

    def create(
            self,
            username: Username,
            raw_password: UserRawPassword,
            role: UserRole = UserRole.USER,
            is_active: bool = True,
    ) -> User:
        ...