import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.double_square_whitestone import DoubleSquareWhitestoneEncryptView
from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.services.cipher_table_service import CipherTableService
from cryptography_methods.domain.common.values.text import Text
from cryptography_methods.domain.double_square_whitestone.entities.double_table import DoubleTableWhitestone
from cryptography_methods.domain.double_square_whitestone.services.double_square_whitestone_service import (
    DoubleSquareWhitestoneService
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class EncryptDoubleSquareWhitestoneCommand:
    text: str
    left_table: list[list[str]]
    right_table: list[list[str]]


@final
class EncryptDoubleSquareWhitestoneCommandHandler:
    def __init__(
            self,
            double_square_whitestone_service: DoubleSquareWhitestoneService,
            cipher_table_service: CipherTableService,
    ) -> None:
        self._double_whitestone_service: Final[DoubleSquareWhitestoneService] = double_square_whitestone_service
        self._cipher_table_service: Final[CipherTableService] = cipher_table_service

    async def __call__(self, data: EncryptDoubleSquareWhitestoneCommand) -> DoubleSquareWhitestoneEncryptView:
        logger.info("Started encryption using double square whitestone")

        cleared_text: str = data.text.replace("Й", "И").replace("й", "и")
        logger.info("Replaced all Й on И: %s", cleared_text)

        if len(cleared_text) % 2 != 0:
            logger.info("Length of cleared text is not even, adding space at the end")
            cleared_text += " "

        text_for_encryption: Text = Text(cleared_text)
        logger.info("Validated text for encryption: %s", text_for_encryption)

        left_table: Table = self._cipher_table_service.create(
            width=len(data.left_table[0]),
            height=len(data.left_table),
            data="".join(column for row in data.left_table for column in row)
        )

        right_table: Table = self._cipher_table_service.create(
            width=len(data.left_table[0]),
            height=len(data.right_table),
            data="".join(column for row in data.right_table for column in row)
        )

        double_table_whitestone: DoubleTableWhitestone = self._double_whitestone_service.create_with_tables(
            left_table=left_table,
            right_table=right_table,
        )

        encrypted_text: Text = self._double_whitestone_service.encrypt(
            text=text_for_encryption,
            key_for_encryption=double_table_whitestone
        )

        return DoubleSquareWhitestoneEncryptView(
            text=data.text,
            encrypted_text=encrypted_text.value,
            left_table=data.left_table,
            right_table=data.right_table,
        )
