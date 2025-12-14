"""Сервис для шифрования и дешифрования по ГОСТ 28147-89."""
import logging
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.gost_28147.services.bit_utils import Gost28147BitUtils
from cryptography_methods.domain.gost_28147.services.feistel_cipher import FeistelCipher
from cryptography_methods.domain.gost_28147.services.substitution_table import Gost28147SubstitutionTable

logger: Final[logging.Logger] = logging.getLogger(__name__)


class Gost28147Service(DomainService):
    """Сервис для шифрования и дешифрования по ГОСТ 28147-89."""

    def __init__(self) -> None:
        super().__init__()
        self._bit_utils: Final[Gost28147BitUtils] = Gost28147BitUtils()
        self._substitution_table: Final[Gost28147SubstitutionTable] = Gost28147SubstitutionTable(
            self._bit_utils
        )
        self._feistel_cipher: Final[FeistelCipher] = FeistelCipher(
            self._bit_utils,
            self._substitution_table
        )

    def encrypt(self, data: bytes, key: bytes) -> bytes:
        """Шифрует данные по ГОСТ 28147-89.

        Args:
            data: Данные для шифрования
            key: Ключ шифрования (32 байта)

        Returns:
            Зашифрованные данные
        """
        logger.info("Started encryption using GOST 28147-89. Data length: %d bytes", len(data))
        return self._process(data, key, is_encryption=True)

    def decrypt(self, data: bytes, key: bytes) -> bytes:
        """Дешифрует данные по ГОСТ 28147-89.

        Args:
            data: Данные для дешифрования
            key: Ключ шифрования (32 байта)

        Returns:
            Расшифрованные данные
        """
        logger.info("Started decryption using GOST 28147-89. Data length: %d bytes", len(data))
        return self._process(data, key, is_encryption=False)

    def _process(self, data: bytes, key: bytes, is_encryption: bool) -> bytes:
        """Обрабатывает данные (шифрование или дешифрование).

        Args:
            data: Данные для обработки
            key: Ключ шифрования (32 байта)
            is_encryption: True для шифрования, False для дешифрования

        Returns:
            Обработанные данные
        """
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes (256 bits)")

        # Дополняем данные до кратного 8 байтам
        padded_length = len(data)
        if padded_length % 8 != 0:
            padded_length = padded_length + (8 - (padded_length % 8))
            logger.debug(f"Padding data from {len(data)} to {padded_length} bytes")

        # Разбиваем ключ на 8 32-битных слов
        keys32b = self._bit_utils.split_256_bits_to_32_bits(key)
        logger.debug(f"Split key into {len(keys32b)} 32-bit words")

        result = bytearray()
        block_count = padded_length // 8
        logger.info(f"Processing {block_count} blocks of 8 bytes each")

        for block_idx in range(0, padded_length, 8):
            # Берем блок из 8 байт
            block = bytearray(8)
            bytes_to_copy = min(8, len(data) - block_idx)
            block[:bytes_to_copy] = data[block_idx:block_idx + bytes_to_copy]
            
            # Дополняем пробелами если нужно
            if bytes_to_copy < 8:
                for j in range(bytes_to_copy, 8):
                    block[j] = 0x20  # пробел
                logger.debug(f"Block {block_idx // 8}: padded {8 - bytes_to_copy} bytes")

            logger.debug(f"Processing block {block_idx // 8}: {block.hex()}")

            # Преобразуем блок в 64-битное число
            block64b = self._bit_utils.join_8_bits_to_64_bits(block)
            n1, n2 = self._bit_utils.split_64_bits_to_32_bits(block64b)

            # Применяем сеть Фейстеля
            if is_encryption:
                n1, n2 = self._feistel_cipher.encrypt(n1, n2, keys32b)
            else:
                n1, n2 = self._feistel_cipher.decrypt(n1, n2, keys32b)

            # Преобразуем обратно в байты
            result_block64b = self._bit_utils.join_32_bits_to_64_bits(n1, n2)
            result_bytes = self._bit_utils.split_64_bits_to_8_bits(result_block64b)
            result.extend(result_bytes)
            
            logger.debug(f"Block {block_idx // 8} processed: {result_bytes.hex()}")

        logger.info(f"Processing completed. Result length: {len(result)} bytes")
        return bytes(result)
