from typing import cast
from uuid import uuid4

from typing_extensions import override

from compressor.domain.users.ports.user_id_generator import UserIDGenerator
from compressor.domain.users.values.user_id import UserID


class UUID4UserIDGenerator(UserIDGenerator):
    @override
    async def __call__(self) -> UserID:
        return cast(UserID, uuid4())
