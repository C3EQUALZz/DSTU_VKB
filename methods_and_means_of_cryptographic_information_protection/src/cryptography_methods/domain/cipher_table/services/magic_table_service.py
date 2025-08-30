import logging
from typing import Final

from cryptography_methods.domain.cipher_table.entities.table import Table
from cryptography_methods.domain.cipher_table.values.magic_table import MagicTable
from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.common.values.text import Text

logger: Final[logging.Logger] = logging.getLogger(__name__)


class MagicTableService(DomainService):
    def __init__(self) -> None:
        super().__init__()

    def encrypt(self, data: Text, magic_table: MagicTable) -> Text:

        table_with_encrypted_chars: list[list[str]] = [
            ["" for _ in range(magic_table.width)]
            for _ in range(magic_table.height)
        ]

        logger.info("Created empty table for store encrypted chars: %s", table_with_encrypted_chars)

        for row_index in range(len(magic_table)):
            for column_index in range(len(magic_table[row_index])):
                logger.info(
                    "row index: %s, column index: %s, magic_table[row_index][column_index]: %s",
                    row_index,
                    column_index,
                    magic_table[row_index][column_index],
                )
                table_with_encrypted_chars[row_index][column_index] = data[magic_table[row_index][column_index] - 1]
                logger.info("New encrypted char: %s", table_with_encrypted_chars[row_index][column_index])

        return Text(''.join((''.join(row) for row in table_with_encrypted_chars)))

    def decrypt(self, data: Text, magic_table: Table) -> Text:
        ...
