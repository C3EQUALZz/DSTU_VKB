"""Сеть Фейстеля для ГОСТ 28147-89."""
import logging
from typing import Final

from cryptography_methods.domain.gost_28147.services.bit_utils import Gost28147BitUtils
from cryptography_methods.domain.gost_28147.services.substitution_table import Gost28147SubstitutionTable

logger: Final[logging.Logger] = logging.getLogger(__name__)


class FeistelCipher:
    """Класс для реализации сети Фейстеля ГОСТ 28147-89."""

    def __init__(
        self,
        bit_utils: Gost28147BitUtils,
        substitution_table: Gost28147SubstitutionTable
    ) -> None:
        self._bit_utils: Final[Gost28147BitUtils] = bit_utils
        self._substitution_table: Final[Gost28147SubstitutionTable] = substitution_table

    def encrypt(self, n1: int, n2: int, keys32b: list[int]) -> tuple[int, int]:
        """Применяет сеть Фейстеля для шифрования.

        Args:
            n1: Первое 32-битное слово
            n2: Второе 32-битное слово
            keys32b: Массив из 8 32-битных ключей

        Returns:
            Кортеж из преобразованных n1 и n2
        """
        logger.info(f"Starting Feistel encryption: N1=0x{n1:08X}, N2=0x{n2:08X}")
        # Шифрование: 24 раунда с ключами 0-7, затем 8 раундов с ключами 7-0
        for round_num in range(24):
            n1, n2 = self._round(n1, n2, keys32b, round_num)
        for round_num in range(31, 23, -1):  # от 31 до 24 включительно
            n1, n2 = self._round(n1, n2, keys32b, round_num)
        logger.info(f"Feistel encryption completed: N1=0x{n1:08X}, N2=0x{n2:08X}")
        return n1, n2

    def decrypt(self, n1: int, n2: int, keys32b: list[int]) -> tuple[int, int]:
        """Применяет сеть Фейстеля для дешифрования.

        Args:
            n1: Первое 32-битное слово
            n2: Второе 32-битное слово
            keys32b: Массив из 8 32-битных ключей

        Returns:
            Кортеж из преобразованных n1 и n2
        """
        logger.info(f"Starting Feistel decryption: N1=0x{n1:08X}, N2=0x{n2:08X}")
        # Дешифрование: 8 раундов с ключами 0-7, затем 24 раунда с ключами 7-0
        for round_num in range(8):
            n1, n2 = self._round(n1, n2, keys32b, round_num)
        for round_num in range(31, 7, -1):  # от 31 до 8 включительно
            n1, n2 = self._round(n1, n2, keys32b, round_num)
        logger.info(f"Feistel decryption completed: N1=0x{n1:08X}, N2=0x{n2:08X}")
        return n1, n2

    def _round(self, n1: int, n2: int, keys32b: list[int], round_num: int) -> tuple[int, int]:
        """Выполняет один раунд сети Фейстеля.

        Args:
            n1: Первое 32-битное слово
            n2: Второе 32-битное слово
            keys32b: Массив из 8 32-битных ключей
            round_num: Номер раунда

        Returns:
            Кортеж из преобразованных n1 и n2
        """
        key = keys32b[round_num % 8]
        logger.debug(f"Round {round_num}: N1=0x{n1:08X}, N2=0x{n2:08X}, Key=0x{key:08X}")

        # Сложение по модулю 2^32 (32-битное переполнение)
        result = (n1 + key) & 0xFFFFFFFF
        logger.debug(f"After addition: 0x{result:08X}")

        # Применение S-блоков
        result = self._substitution_table.apply(result)
        logger.debug(f"After S-box: 0x{result:08X}")

        # Циклический сдвиг влево на 11 бит
        result = self._bit_utils.lshift_n_bit(result, 11, 32)
        logger.debug(f"After left shift: 0x{result:08X}")

        # XOR с N2 и замена
        temp = n1
        new_n1 = result ^ n2
        new_n2 = temp
        logger.debug(f"After XOR and swap: N1=0x{new_n1:08X}, N2=0x{new_n2:08X}")

        return new_n1, new_n2

