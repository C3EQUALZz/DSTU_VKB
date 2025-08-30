import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.magic_table import MagicTableEncryptView
from cryptography_methods.domain.cipher_table.services.magic_table_service import MagicTableService
from cryptography_methods.domain.cipher_table.values.magic_table import MagicTable
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class MagicTableEncryptCommand:
    text: str
    table: list[list[int]]


@final
class MagicTableEncryptCommandHandler:
    def __init__(self, magic_table_service: MagicTableService) -> None:
        self._magic_table_service: Final[MagicTableService] = magic_table_service

    async def __call__(self, data: MagicTableEncryptCommand) -> MagicTableEncryptView:
        logger.info("Started encryption for magic table")
        validated_text: Text = Text(data.text)
        logger.info("Validated encrypted text %s", validated_text)
        magic_table: MagicTable = MagicTable(data.table)
        logger.info("Built magic table %s", magic_table)

        encrypted_text: Text = self._magic_table_service.encrypt(
            data=validated_text,
            magic_table=magic_table,
        )

        logger.info("Finished Magic Table. Encrypted text %s", encrypted_text)

        return MagicTableEncryptView(
            text=data.text,
            encrypted_text=encrypted_text.value,
            magic_table=data.table,
        )
