from typing import Final

from compressor.domain.common.services.base import DomainService
from compressor.domain.users.entities.user import User
from compressor.domain.users.errors import RoleAssignmentNotPermittedError, CantChangeUsernameError
from compressor.domain.users.ports.password_hasher import PasswordHasher
from compressor.domain.users.ports.user_id_generator import UserIDGenerator
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_password_hash import UserPasswordHash
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
        if not role.is_assignable:
            msg: str = f"Assignment of role {role} is not permitted."
            raise RoleAssignmentNotPermittedError(msg)

        user_id: UserID = self._user_id_generator()
        password_hash: UserPasswordHash = self._password_hasher.hash(raw_password)

        return User(
            id=user_id,
            username=username,
            role=role,
            is_active=is_active,
            password_hash=password_hash,
        )

    def is_password_valid(self, raw_password: UserRawPassword, user: User) -> bool:
        return self._password_hasher.verify(
            raw_password=raw_password,
            hashed_password=user.password_hash,
        )

    def change_password(self, user: User, raw_password: UserRawPassword) -> None:
        hashed_password: UserPasswordHash = self._password_hasher.hash(raw_password)
        user.password_hash = hashed_password

    # noinspection PyMethodMayBeStatic
    def change_username(self, user: User, new_username: Username) -> None:
        if user.role == UserRole.SUPER_ADMIN:
            msg: str = f"User {user.username} is not allowed to change username."
            raise CantChangeUsernameError(msg)
        user.username = new_username
