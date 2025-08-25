from dataclasses import dataclass
from typing import final

from compressor.application.common.views.users import CreateUserView
from compressor.domain.users.values.user_role import UserRole


@dataclass(frozen=True, slots=True, kw_only=True)
class CreateUserCommand:
    username: str
    password: str
    role: UserRole


@final
class CreateUserCommandHandler:
    def __init__(self) -> None:
        ...

    async def __call__(self, data: CreateUserCommand) -> CreateUserView:
        ...
