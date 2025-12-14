"""Утилиты для работы с битами и байтами в ГОСТ 28147-89."""
import logging
import struct
from typing import Final

logger: Final[logging.Logger] = logging.getLogger(__name__)


class Gost28147BitUtils:
    """Утилиты для преобразования битов и байтов."""

    @staticmethod
    def split_256_bits_to_32_bits(key256b: bytes) -> list[int]:
        """Разбивает 256-битный ключ на 8 32-битных слов.

        Args:
            key256b: 256-битный ключ (32 байта)

        Returns:
            Список из 8 32-битных слов
        """
        logger.debug("Splitting 256-bit key into 8 32-bit words")
        keys32b = []
        for i in range(8):
            # Используем little-endian порядок байтов
            key32b = struct.unpack('<I', key256b[i * 4:(i + 1) * 4])[0]
            keys32b.append(key32b)
            logger.debug(f"Key word {i}: 0x{key32b:08X}")
        return keys32b

    @staticmethod
    def split_64_bits_to_32_bits(block64b: int) -> tuple[int, int]:
        """Разбивает 64-битный блок на два 32-битных слова.

        Args:
            block64b: 64-битный блок

        Returns:
            Кортеж из двух 32-битных слов (N1, N2)
        """
        block32b_2 = block64b & 0xFFFFFFFF
        block32b_1 = (block64b >> 32) & 0xFFFFFFFF
        logger.debug(f"Splitting 64-bit block: N1=0x{block32b_1:08X}, N2=0x{block32b_2:08X}")
        return block32b_1, block32b_2

    @staticmethod
    def join_8_bits_to_64_bits(blocks8b: bytearray) -> int:
        """Объединяет 8 байт в 64-битное число.

        Args:
            blocks8b: Массив из 8 байт

        Returns:
            64-битное число
        """
        block64b = 0
        for i in range(8):
            block64b = (block64b << 8) | blocks8b[i]
        logger.debug(f"Joining 8 bytes to 64-bit: 0x{block64b:016X}")
        return block64b

    @staticmethod
    def join_32_bits_to_64_bits(block32b_1: int, block32b_2: int) -> int:
        """Объединяет два 32-битных слова в 64-битное число.

        Args:
            block32b_1: Первое 32-битное слово
            block32b_2: Второе 32-битное слово

        Returns:
            64-битное число
        """
        result = ((block32b_2 & 0xFFFFFFFF) << 32) | (block32b_1 & 0xFFFFFFFF)
        logger.debug(f"Joining 32-bit words to 64-bit: 0x{result:016X}")
        return result

    @staticmethod
    def split_64_bits_to_8_bits(block64b: int) -> bytearray:
        """Разбивает 64-битный блок на 8 байт.

        Args:
            block64b: 64-битный блок

        Returns:
            Массив из 8 байт
        """
        blocks8b = bytearray(8)
        for i in range(8):
            blocks8b[i] = (block64b >> ((7 - i) * 8)) & 0xFF
        logger.debug(f"Splitting 64-bit block to 8 bytes: {blocks8b.hex()}")
        return blocks8b

    @staticmethod
    def split_32_bits_to_4_bits(block32b: int) -> list[int]:
        """Разбивает 32-битный блок на 8 4-битных блоков.

        Args:
            block32b: 32-битный блок

        Returns:
            Массив из 8 4-битных блоков
        """
        blocks4b = []
        for i in range(8):
            blocks4b.append((block32b >> (4 * (7 - i))) & 0x0F)
        return blocks4b

    @staticmethod
    def join_4_bits_to_32_bits(blocks4b: list[int]) -> int:
        """Объединяет 8 4-битных блоков в 32-битное число.

        Args:
            blocks4b: Массив из 8 4-битных блоков

        Returns:
            32-битное число
        """
        block32b = 0
        for i in range(8):
            block32b |= (blocks4b[i] << (4 * (7 - i)))
        return block32b

    @staticmethod
    def lshift_n_bit(x: int, l: int, n: int = 32) -> int:
        """Выполняет циклический сдвиг влево на L бит.

        Args:
            x: Число для сдвига
            l: Количество бит для сдвига
            n: Размерность числа в битах (по умолчанию 32)

        Returns:
            Результат циклического сдвига
        """
        result = ((x << l) | (x >> (n - l))) & ((1 << n) - 1)
        logger.debug(f"Left shift {l} bits: 0x{x:08X} -> 0x{result:08X}")
        return result

