"""Сервис для протокола идентификации с нулевой передачей данных."""
import logging
import secrets
from dataclasses import dataclass
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService
)
from cryptography_methods.domain.zero_knowledge_proof.services.quadratic_residue_service import (
    QuadraticResidueService
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ProtocolKeys:
    """Ключи протокола."""

    p: int
    q: int
    n: int
    v: int  # Открытый ключ (квадратичный вычет)
    s: int  # Закрытый ключ


@dataclass(frozen=True, slots=True)
class ProtocolIterationResult:
    """Результат одной итерации протокола."""

    iteration_number: int
    r: int
    x: int
    b: int
    y: int | None
    verification_passed: bool


@dataclass(frozen=True, slots=True)
class ProtocolResult:
    """Результат выполнения протокола."""

    keys: ProtocolKeys
    iterations: list[ProtocolIterationResult]
    total_iterations: int
    failed_attempts: int
    failure_rate: float
    authentication_passed: bool


class ZeroKnowledgeProofService(DomainService):
    """Сервис для выполнения протокола идентификации с нулевой передачей данных."""

    def __init__(
        self,
        prime_number_service: PrimeNumberService,
        quadratic_residue_service: QuadraticResidueService,
        modular_arithmetic_service: ModularArithmeticService
    ) -> None:
        super().__init__()
        self._prime_service: Final[PrimeNumberService] = prime_number_service
        self._quadratic_service: Final[QuadraticResidueService] = quadratic_residue_service
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service

    def generate_keys(self, bit_length: int = 256) -> ProtocolKeys:
        """Генерирует ключи для протокола.

        Args:
            bit_length: Длина простых чисел в битах

        Returns:
            Ключи протокола
        """
        logger.info(f"Generating protocol keys with {bit_length}-bit primes")

        # Генерируем простые числа
        p = self._prime_service.generate_large_prime(bit_length)
        q = self._prime_service.generate_large_prime(bit_length)
        n = p * q

        logger.info(f"Generated primes: p = {p}, q = {q}, n = {n}")

        # Проверяем простоту
        if not self._prime_service.miller_rabin_test(p, 5):
            raise ValueError("p is not prime")
        if not self._prime_service.miller_rabin_test(q, 5):
            raise ValueError("q is not prime")

        # Находим квадратичный вычет V
        logger.info("Finding random quadratic residue V")
        v = self._quadratic_service.find_random_quadratic_residue(n, p, q)
        logger.info(f"Found quadratic residue V: {v}")

        # Вычисляем обратный элемент V^(-1) mod n
        inverse_v = self._modular_arithmetic.mod_inverse(v, n)
        if inverse_v is None:
            raise ValueError("Cannot find modular inverse for V")

        # Вычисляем квадратный корень из V^(-1) mod n
        logger.info("Computing secret key S")
        s = self._quadratic_service.find_square_root_mod_n(inverse_v, n, p, q)
        if s is None:
            raise ValueError("Cannot find square root for V^(-1)")

        logger.info(f"Secret key S: {s}")

        return ProtocolKeys(p=p, q=q, n=n, v=v, s=s)

    def execute_single_iteration(
        self,
        keys: ProtocolKeys,
        r: int,
        iteration_number: int,
        wrong_secret_key: int | None = None
    ) -> ProtocolIterationResult:
        """Выполняет одну итерацию протокола.

        Args:
            keys: Ключи протокола
            r: Случайное число r
            iteration_number: Номер итерации
            wrong_secret_key: Неправильный секретный ключ для тестирования (если None, используется правильный)

        Returns:
            Результат итерации
        """
        logger.info(f"Executing iteration {iteration_number}")

        # Вычисляем x = r² mod n
        x = self._modular_arithmetic.mod_pow(r, 2, keys.n)
        logger.debug(f"A → B: x = r² mod n = {x}")

        # Генерируем случайный бит b
        b = secrets.randbelow(2)
        logger.debug(f"B → A: b = {b}")

        # Выполняем шаг протокола
        return self._execute_protocol_step(keys, r, x, b, iteration_number, wrong_secret_key)

    def execute_protocol(
        self,
        keys: ProtocolKeys,
        iterations: int,
        random_values: list[int] | None = None
    ) -> ProtocolResult:
        """Выполняет протокол идентификации.

        Args:
            keys: Ключи протокола
            iterations: Количество итераций
            random_values: Список случайных значений r (опционально, для тестирования)

        Returns:
            Результат выполнения протокола
        """
        logger.info(f"Executing protocol with {iterations} iterations")
        protocol_results: list[ProtocolIterationResult] = []
        failed_attempts = 0
        used_r: set[int] = set()

        for i in range(iterations):
            logger.info(f"Iteration {i + 1}/{iterations}")

            # Генерируем или используем предоставленное значение r
            if random_values and i < len(random_values):
                r = random_values[i]
                logger.debug(f"Using provided r: {r}")
            else:
                r = self._generate_random_r(keys.n, used_r)
                logger.debug(f"Generated random r: {r}")

            used_r.add(r)

            # Вычисляем x = r² mod n
            x = self._modular_arithmetic.mod_pow(r, 2, keys.n)
            logger.debug(f"A → B: x = r² mod n = {x}")

            # Генерируем случайный бит b
            b = secrets.randbelow(2)
            logger.debug(f"B → A: b = {b}")

            # Выполняем шаг протокола
            iteration_result = self._execute_protocol_step(keys, r, x, b, i + 1)
            protocol_results.append(iteration_result)

            if not iteration_result.verification_passed:
                failed_attempts += 1
                logger.warning(f"Iteration {i + 1} failed verification")

        failure_rate = failed_attempts / iterations
        authentication_passed = failure_rate <= 0.01

        logger.info(
            f"Protocol completed: {failed_attempts}/{iterations} failed attempts, "
            f"failure rate: {failure_rate:.2%}, "
            f"authentication: {'PASSED' if authentication_passed else 'FAILED'}"
        )

        return ProtocolResult(
            keys=keys,
            iterations=protocol_results,
            total_iterations=iterations,
            failed_attempts=failed_attempts,
            failure_rate=failure_rate,
            authentication_passed=authentication_passed
        )

    def _execute_protocol_step(
        self,
        keys: ProtocolKeys,
        r: int,
        x: int,
        b: int,
        iteration_number: int,
        wrong_secret_key: int | None = None
    ) -> ProtocolIterationResult:
        """Выполняет один шаг протокола.

        Args:
            keys: Ключи протокола
            r: Случайное число
            x: x = r² mod n
            b: Случайный бит (0 или 1)
            iteration_number: Номер итерации
            wrong_secret_key: Неправильный секретный ключ для тестирования (если None, используется правильный)

        Returns:
            Результат итерации
        """
        y: int | None = None
        verification_passed = False

        if b == 0:
            # A отправляет r, B проверяет x = r² mod n
            logger.debug(f"A → B: r = {r}")
            x1 = self._modular_arithmetic.mod_pow(r, 2, keys.n)

            if x1 == x:
                verification_passed = True
                logger.debug("B: Verification passed (x = r² mod n)")
            else:
                logger.warning(f"B: Verification failed! Expected {x}, got {x1}")
        else:
            # A отправляет y = r * S mod n, B проверяет x = y² * V mod n
            # Если передан неправильный ключ, используем его для симуляции обмана
            secret_key = wrong_secret_key if wrong_secret_key is not None else keys.s
            y = (r * secret_key) % keys.n
            logger.debug(f"A → B: y = r * S mod n = {y}")

            x1 = (y * y * keys.v) % keys.n

            if x1 == x:
                verification_passed = True
                logger.debug("B: Verification passed (y² * V mod n = x)")
            else:
                logger.warning(f"B: Verification failed! Expected {x}, got {x1}")

        return ProtocolIterationResult(
            iteration_number=iteration_number,
            r=r,
            x=x,
            b=b,
            y=y,
            verification_passed=verification_passed
        )

    def _generate_random_r(self, n: int, used_r: set[int]) -> int:
        """Генерирует случайное число r в диапазоне (0, n), не использовавшееся ранее.

        Args:
            n: Модуль
            used_r: Множество уже использованных значений r

        Returns:
            Случайное число r
        """
        import secrets

        max_attempts = 1000
        attempt = 0

        while attempt < max_attempts:
            range_size = n - 1
            num_bytes = (range_size.bit_length() + 7) // 8

            random_bytes = secrets.token_bytes(num_bytes)
            candidate = int.from_bytes(random_bytes, byteorder='big')
            r = 1 + (candidate % range_size)

            if r not in used_r:
                return r
            attempt += 1

        raise RuntimeError(f"Failed to generate unique r after {max_attempts} attempts")

