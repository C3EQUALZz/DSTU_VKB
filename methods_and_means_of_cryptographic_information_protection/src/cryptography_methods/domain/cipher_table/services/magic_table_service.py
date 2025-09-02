import logging
from typing import Final

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

    def decrypt(self, data: Text, magic_table: MagicTable) -> Text:
        """
        Дешифрование с использованием магического квадрата.

        Args:
            data: зашифрованный текст
            magic_table: магический квадрат с числами от 1 до n²

        Returns:
            Расшифрованный текст
        """
        # Создаем таблицу для зашифрованных символов (построчно из данных)
        encrypted_table: list[list[str]] = [
            ["" for _ in range(magic_table.width)]
            for _ in range(magic_table.height)
        ]

        logger.info("Created empty table for encrypted chars: %s", encrypted_table)

        # Заполняем таблицу зашифрованными символами построчно
        data_index: int = 0
        for row_index in range(magic_table.height):
            for column_index in range(magic_table.width):
                encrypted_table[row_index][column_index] = data.value[data_index]
                data_index += 1

        logger.info("Filled encrypted table: %s", encrypted_table)

        # Создаем список для расшифрованных символов
        # Длина равна количеству ячеек в магическом квадрате
        decrypted_chars = [""] * (magic_table.width * magic_table.height)
        logger.info("Created empty list for store decrypted chars: %s", decrypted_chars)

        # Заполняем decrypted_chars в правильном порядке с помощью магического квадрата
        logger.info("Started filling decrypted chars: %s", decrypted_chars)
        for row_index in range(magic_table.height):
            for column_index in range(magic_table.width):
                # Получаем позицию в исходном тексте из магического квадрата
                original_position: int = magic_table[row_index][column_index] - 1
                logger.info(
                    "row index: %s, column index: %s, original_position: %s",
                    row_index,
                    column_index,
                    original_position
                )
                decrypted_chars[original_position] = encrypted_table[row_index][column_index]
                logger.info("New decrypted char: %s", decrypted_chars[original_position])
                logger.info("Updated decrypted chars: %s", decrypted_chars)

        logger.info("Decrypted chars: %s", decrypted_chars)

        return Text(''.join(decrypted_chars).rstrip())
