from typing import cast
from uuid import uuid4

from cryptography_methods.domain.double_square_whitestone.services.id_generator import DoubleTableWhitestoneIdGenerator
from cryptography_methods.domain.double_square_whitestone.values.table_id import WhiteStoneTableID


class UUID4TableWhiteStoneIDGenerator(DoubleTableWhitestoneIdGenerator):
    def __call__(self) -> WhiteStoneTableID:
        return cast(WhiteStoneTableID, uuid4())
