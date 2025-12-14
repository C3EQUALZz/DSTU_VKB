"""Сервис для работы с простыми числами."""
import logging
import secrets
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class PrimeNumberService(DomainService):
    """Сервис для генерации и проверки простых чисел."""

    def __init__(self, modular_arithmetic_service: ModularArithmeticService) -> None:
        super().__init__()
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service

    def generate_large_prime(self, bit_length: int) -> int:
        """Генерирует большое простое число заданной битовой длины.

        Args:
            bit_length: Длина числа в битах

        Returns:
            Простое число
        """
        logger.info(f"Generating large prime number with {bit_length} bits")
        max_attempts = 1000
        attempt = 0

        while attempt < max_attempts:
            candidate = self._generate_random_big_integer(bit_length)
            logger.debug(f"Attempt {attempt + 1}: Testing candidate {candidate}")

            if self.miller_rabin_test(candidate, k=5):
                logger.info(f"Found prime number: {candidate}")
                return candidate

            attempt += 1

        raise RuntimeError(f"Failed to generate prime number after {max_attempts} attempts")

    def miller_rabin_test(self, n: int, k: int = 5) -> bool:
        """Тест Миллера-Рабина для проверки простоты числа.

        Args:
            n: Число для проверки
            k: Количество итераций теста

        Returns:
            True если число вероятно простое, False если составное
        """
        logger.debug(f"Miller-Rabin test for {n} with {k} iterations")

        if n <= 2:
            result = n == 2
            logger.debug(f"n <= 2, result: {result}")
            return result

        if n == 3:
            logger.debug("n == 3, result: True")
            return True

        # Записываем n - 1 = d * 2^s
        d = n - 1
        s = 0

        while d % 2 == 0:
            d //= 2
            s += 1

        logger.debug(f"n - 1 = {d} * 2^{s}")

        for i in range(k):
            a = self._generate_random_big_integer_in_range(2, n - 2)
            logger.debug(f"Iteration {i + 1}: Testing with a = {a}")

            x = self._modular_arithmetic.mod_pow(a, d, n)

            if x == 1 or x == n - 1:
                logger.debug(f"x = {x}, continuing")
                continue

            for j in range(s - 1):
                x = self._modular_arithmetic.mod_pow(x, 2, n)
                if x == n - 1:
                    logger.debug(f"x = {x} at iteration {j + 1}, breaking")
                    break
            else:
                logger.debug(f"Composite number detected at iteration {i + 1}")
                return False

        logger.debug(f"Number {n} is probably prime")
        return True

    def _generate_random_big_integer(self, bit_length: int) -> int:
        """Генерирует случайное большое число заданной битовой длины.

        Args:
            bit_length: Длина числа в битах

        Returns:
            Случайное число
        """
        min_value = 1 << (bit_length - 1)
        max_value = 1 << bit_length
        return self._generate_random_big_integer_in_range(min_value, max_value)

    def _generate_random_big_integer_in_range(self, min_value: int, max_value: int) -> int:
        """Генерирует случайное число в заданном диапазоне.

        Args:
            min_value: Минимальное значение (включительно)
            max_value: Максимальное значение (исключительно)

        Returns:
            Случайное число в диапазоне [min_value, max_value)
        """
        range_size = max_value - min_value
        num_bytes = (range_size.bit_length() + 7) // 8

        while True:
            random_bytes = secrets.token_bytes(num_bytes)
            candidate = int.from_bytes(random_bytes, byteorder='big')
            candidate = min_value + (candidate % range_size)

            if min_value <= candidate < max_value:
                return candidate

