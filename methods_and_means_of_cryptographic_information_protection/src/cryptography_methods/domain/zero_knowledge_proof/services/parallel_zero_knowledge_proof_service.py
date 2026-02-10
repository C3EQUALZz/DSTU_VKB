"""Сервис для параллельной схемы протокола идентификации с нулевой передачей данных."""
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
class ParallelProtocolKeys:
    """Ключи параллельной схемы протокола."""

    p: int
    q: int
    n: int
    public_keys: list[int]   # V1, V2, ..., VK (открытые ключи — квадратичные вычеты)
    secret_keys: list[int]   # S1, S2, ..., SK (секретные ключи)
    k: int                   # количество ключей


@dataclass(frozen=True, slots=True)
class ParallelProtocolIterationResult:
    """Результат одной итерации параллельной схемы протокола."""

    iteration_number: int
    r: int
    x: int
    bits: list[int]          # b1, b2, ..., bK
    y: int
    verification_passed: bool


class ParallelZeroKnowledgeProofService(DomainService):
    """Сервис для параллельной схемы протокола идентификации с нулевой передачей данных."""

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

    def generate_keys(self, bit_length: int, k: int) -> ParallelProtocolKeys:
        """Генерирует ключи для параллельной схемы протокола.

        Args:
            bit_length: Длина простых чисел в битах
            k: Количество пар ключей (V, S)

        Returns:
            Ключи протокола
        """
        logger.info(f"Generating parallel protocol keys: {bit_length}-bit primes, K={k}")

        # Генерируем простые числа p, q и модуль n
        p = self._prime_service.generate_large_prime(bit_length)
        q = self._prime_service.generate_large_prime(bit_length)
        n = p * q

        logger.info(f"Generated primes: p = {p}, q = {q}, n = {n}")

        if not self._prime_service.miller_rabin_test(p, 5):
            raise ValueError("p is not prime")
        if not self._prime_service.miller_rabin_test(q, 5):
            raise ValueError("q is not prime")

        # Генерируем K пар (Vi, Si)
        public_keys: list[int] = []
        secret_keys: list[int] = []
        used_v: set[int] = set()

        for i in range(k):
            # Находим уникальный квадратичный вычет Vi
            max_attempts = 1000
            v: int | None = None
            for _ in range(max_attempts):
                candidate = self._quadratic_service.find_random_quadratic_residue(n, p, q)
                if candidate not in used_v:
                    v = candidate
                    used_v.add(v)
                    break

            if v is None:
                raise RuntimeError(f"Не удалось найти уникальный квадратичный вычет V{i + 1}")

            # Вычисляем Vi^(-1) mod n
            inverse_v = self._modular_arithmetic.mod_inverse(v, n)
            if inverse_v is None:
                raise ValueError(f"Cannot find modular inverse for V{i + 1}={v}")

            # Вычисляем Si = √(Vi^(-1)) mod n (наименьшее значение)
            s = self._quadratic_service.find_square_root_mod_n(inverse_v, n, p, q)
            if s is None:
                raise ValueError(f"Cannot find square root for V{i + 1}^(-1)")

            public_keys.append(v)
            secret_keys.append(s)

            logger.info(f"Key pair {i + 1}: V{i + 1}={v}, S{i + 1}={s}")

        return ParallelProtocolKeys(
            p=p, q=q, n=n,
            public_keys=public_keys,
            secret_keys=secret_keys,
            k=k,
        )

    def execute_single_iteration(
        self,
        keys: ParallelProtocolKeys,
        r: int,
        iteration_number: int,
        wrong_secret_keys: list[int] | None = None,
    ) -> ParallelProtocolIterationResult:
        """Выполняет одну итерацию параллельной схемы протокола.

        Args:
            keys: Ключи протокола
            r: Случайное число r (0 < r < n)
            iteration_number: Номер итерации
            wrong_secret_keys: Неправильные секретные ключи для тестирования

        Returns:
            Результат итерации
        """
        n = keys.n

        # 1. Сторона А вычисляет x = r² mod n
        x = self._modular_arithmetic.mod_pow(r, 2, n)

        # 2. Сторона В генерирует случайную двоичную строку b1, b2, ..., bK
        bits: list[int] = [secrets.randbelow(2) for _ in range(keys.k)]

        # 3. Сторона А вычисляет y = r * (S1^b1 * S2^b2 * ... * SK^bK) mod n
        secret_keys_to_use = wrong_secret_keys if wrong_secret_keys is not None else keys.secret_keys
        y = r
        for j in range(keys.k):
            if bits[j] == 1:
                y = (y * secret_keys_to_use[j]) % n

        # 4. Сторона В проверяет: x = y² * (V1^b1 * V2^b2 * ... * VK^bK) mod n
        check = self._modular_arithmetic.mod_pow(y, 2, n)
        for j in range(keys.k):
            if bits[j] == 1:
                check = (check * keys.public_keys[j]) % n

        verification_passed = (check == x)

        return ParallelProtocolIterationResult(
            iteration_number=iteration_number,
            r=r,
            x=x,
            bits=bits,
            y=y,
            verification_passed=verification_passed,
        )

