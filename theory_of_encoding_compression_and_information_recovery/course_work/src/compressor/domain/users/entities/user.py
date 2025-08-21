from dataclasses import dataclass

from compressor.domain.common.entities.base_entity import BaseEntity
from compressor.domain.users.values.user_id import UserID
from compressor.domain.users.values.user_password_hash import UserPasswordHash
from compressor.domain.users.values.user_role import UserRole


@dataclass(eq=False, kw_only=True)
class User(BaseEntity[UserID]):
    username: Username
    password_hash: UserPasswordHash
    role: UserRole
    is_active: bool