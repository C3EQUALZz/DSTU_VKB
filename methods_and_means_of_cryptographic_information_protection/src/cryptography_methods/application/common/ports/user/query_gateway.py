from typing import Protocol

from cryptography_methods.domain.user.values.user_id import UserID


class UserQueryGateway(Protocol):
    def __init__(self) -> None:
        ...

    async def read_by_id(self, user_id: UserID):
        ...
