import logging
from dataclasses import dataclass
from typing import final, Final

from cryptography_methods.application.common.views.magic_table import MagicTableDecryptView
from cryptography_methods.domain.cipher_table.services.magic_table_service import MagicTableService
from cryptography_methods.domain.cipher_table.values.magic_table import MagicTable
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class MagicTableDecryptCommand:
    text: str
    table: list[list[int]]


@final
class MagicTableDecryptCommandHandler:
    def __init__(self, magic_table_service: MagicTableService) -> None:
        self._magic_table_service: MagicTableService = magic_table_service

    async def __call__(self, data: MagicTableDecryptCommand) -> MagicTableDecryptView:
        logger.info("Started decryption using magic table")
        validated_text: Text = Text(data.text)
        logger.info("Validated text: %s", validated_text)
        magic_table: MagicTable = MagicTable(data.table)
        logger.info("Magic table: %s", magic_table)

        decrypted_text: Text = self._magic_table_service.encrypt(
            data=validated_text,
            magic_table=magic_table,
        )

        logger.info("Finished decryption with magic table. Decrypted text: %s", decrypted_text)

        return MagicTableDecryptView(
            text=data.text,
            decrypted_text=decrypted_text.value,
            magic_table=data.table,
        )
