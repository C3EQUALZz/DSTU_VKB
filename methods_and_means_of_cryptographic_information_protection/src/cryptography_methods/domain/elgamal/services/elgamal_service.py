"""ElGamal public-key cryptosystem service.

Реализует:
* генерацию большого простого числа p;
* поиск (быстрого) первообразного корня g по модулю p;
* генерацию закрытого/открытого ключей (x, y = g^x mod p);
* шифрование и расшифрование байтовых сообщений (как в примере на C#).
"""

import logging
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Final, Iterable

from cryptography_methods.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ElGamalPublicKey:
    p: int
    g: int
    y: int


@dataclass(frozen=True, slots=True)
class ElGamalPrivateKey:
    """ElGamal private key.

    Хранит только показатель x (секретный ключ). Модуль p берётся
    либо из соответствующего публичного ключа, либо из файла ключа.
    """

    x: int


@dataclass(frozen=True, slots=True)
class ElGamalCiphertext:
    """Одна пара (a, b) для зашифрованного байта."""

    a: int
    b: int


class ElGamalService(DomainService):
    """Сервис схемы Эль‑Гамаля, адаптированный под пример на C#."""

    _DEFAULT_KEY_SIZE: Final[int] = 1024
    _DEFAULT_PRIME_CERTAINTY: Final[int] = 10
    _MAX_PRIMITIVE_ROOT_TRIES: Final[int] = 50

    def __init__(self) -> None:
        """Инициализация сервиса ElGamal."""
        super().__init__()
        logger.info(
            "Initialized ElGamalService with defaults: key_size=%s bits, prime_certainty=%s, max_primitive_root_tries=%s",
            self._DEFAULT_KEY_SIZE,
            self._DEFAULT_PRIME_CERTAINTY,
            self._MAX_PRIMITIVE_ROOT_TRIES,
        )

    # ==========================
    #  Публичные методы сервиса
    # ==========================

    def generate_keys(
            self,
            key_size: int | None = None,
            prime_certainty: int | None = None,
    ) -> tuple[ElGamalPublicKey, ElGamalPrivateKey]:
        """Генерация параметров и ключей схемы Эль‑Гамаля.

        Args:
            key_size: размер простого p в битах (по умолчанию 1024)
            prime_certainty: количество раундов Миллера–Рабина

        Returns:
            (public_key, private_key)
        """
        bits = key_size or self._DEFAULT_KEY_SIZE
        certainty = prime_certainty or self._DEFAULT_PRIME_CERTAINTY

        logger.info(
            "Generating ElGamal parameters: key_size=%s bits, prime_certainty=%s",
            bits,
            certainty,
        )

        p = self._generate_prime(bits, certainty)
        logger.debug("ElGamal prime p generated: p=%s", p)

        g = self._find_primitive_root_fast(p)
        logger.debug("ElGamal primitive root g found: g=%s", g)

        x = self._generate_private_key(p)
        logger.debug("ElGamal private key x generated (bits=%s)", x.bit_length())

        y = pow(g, x, p)
        logger.debug("ElGamal public component y computed (bits=%s)", y.bit_length())

        logger.info("Generated parameters: p (bits=%s), g=%s, y=%s", p.bit_length(), g, y)

        return (
            ElGamalPublicKey(p=p, g=g, y=y),
            ElGamalPrivateKey(x=x),
        )

    def encrypt_bytes(
            self,
            message: bytes,
            public_key: ElGamalPublicKey,
    ) -> list[ElGamalCiphertext]:
        """Шифрует последовательность байтов.

        Алгоритм полностью повторяет логику EncryptMessage из C#:
        для каждого байта m выбирается случайный k, вычисляются
        a = g^k mod p, b = (y^k * m) mod p.
        """
        p, g, y = public_key.p, public_key.g, public_key.y

        logger.info("Encrypting message of %d bytes with ElGamal", len(message))
        encrypted: list[ElGamalCiphertext] = []

        for index, m in enumerate(message):
            if m >= p:
                # В нормальном случае p намного больше 256, но оставим защиту.
                raise ValueError("Plaintext byte is greater than or equal to modulus p")

            k = self._random_in_range(2, p - 2)
            a = pow(g, k, p)
            b = (pow(y, k, p) * m) % p
            encrypted.append(ElGamalCiphertext(a=a, b=b))

            # Логируем только первые несколько байтов, чтобы не зашумлять лог.
            if index < 5:
                logger.debug(
                    "Encrypted byte #%d: m=%d, k=%s, a=%s, b=%s",
                    index,
                    m,
                    k,
                    a,
                    b,
                )

        logger.info("Encryption finished, produced %d ciphertext pairs", len(encrypted))
        return encrypted

    def decrypt_bytes(
            self,
            ciphertext: Iterable[ElGamalCiphertext],
            public_modulus_p: int,
            private_key: ElGamalPrivateKey,
    ) -> bytes:
        """Расшифровывает последовательность пар (a, b) в байты.

        Повторяет DecryptMode из C#: используется a^(p-1-x) mod p как обратный элемент.
        """
        p = public_modulus_p
        x = private_key.x

        logger.info(
            "Decrypting ciphertext with ElGamal (p bits=%s, pairs=%s)",
            p.bit_length(),
            len(list(ciphertext)) if not isinstance(ciphertext, list) else len(ciphertext),
        )

        # Если ciphertext — не список (Iterable), материализуем его один раз.
        if not isinstance(ciphertext, list):
            ciphertext = list(ciphertext)

        result = bytearray()
        for index, pair in enumerate(ciphertext):
            exponent = p - 1 - x
            a_inv = pow(pair.a, exponent, p)
            m = (pair.b * a_inv) % p
            if not 0 <= m <= 255:
                raise ValueError(f"Decrypted value {m} is not a valid byte")
            result.append(int(m))

            if index < 5:
                logger.debug(
                    "Decrypted pair #%d: a=%s, b=%s, exponent=%s, a_inv=%s, m=%s",
                    index,
                    pair.a,
                    pair.b,
                    exponent,
                    a_inv,
                    m,
                )

        logger.info("Decryption finished, recovered %d bytes", len(result))
        return bytes(result)

    # ======================
    #  Работа с файлами ключей
    # ======================

    @staticmethod
    def save_public_key(public_key: ElGamalPublicKey, file_path: Path) -> None:
        """Save ElGamal public key to file.

        Формат файла:
            p
            g
            y
        """
        logger.info("Saving ElGamal public key to file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"{public_key.p}\n")
            f.write(f"{public_key.g}\n")
            f.write(f"{public_key.y}\n")

        logger.debug(
            "ElGamal public key saved (p_bits=%s, g=%s, y_bits=%s)",
            public_key.p.bit_length(),
            public_key.g,
            public_key.y.bit_length(),
        )

    @staticmethod
    def save_private_key(p: int, private_key: ElGamalPrivateKey, file_path: Path) -> None:
        """Save ElGamal private key to file.

        Формат файла:
            p
            x
        """
        logger.info("Saving ElGamal private key to file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"{p}\n")
            f.write(f"{private_key.x}\n")

        logger.debug(
            "ElGamal private key saved (p_bits=%s, x_bits=%s)",
            p.bit_length(),
            private_key.x.bit_length(),
        )

    @staticmethod
    def load_public_key(file_path: Path) -> ElGamalPublicKey:
        """Load ElGamal public key from file."""
        logger.info("Loading ElGamal public key from file: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Public key file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 3:
            raise ValueError("Invalid ElGamal public key file format: expected 3 lines (p, g, y)")

        p = int(lines[0])
        g = int(lines[1])
        y = int(lines[2])

        logger.debug(
            "ElGamal public key loaded (p_bits=%s, g=%s, y_bits=%s)",
            p.bit_length(),
            g,
            y.bit_length(),
        )
        return ElGamalPublicKey(p=p, g=g, y=y)

    @staticmethod
    def load_private_key(file_path: Path) -> tuple[int, ElGamalPrivateKey]:
        """Load ElGamal private key from file.

        Returns:
            (p, private_key)
        """
        logger.info("Loading ElGamal private key from file: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Private key file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 2:
            raise ValueError("Invalid ElGamal private key file format: expected 2 lines (p, x)")

        p = int(lines[0])
        x = int(lines[1])

        logger.debug(
            "ElGamal private key loaded (p_bits=%s, x_bits=%s)",
            p.bit_length(),
            x.bit_length(),
        )
        return p, ElGamalPrivateKey(x=x)

    # ======================
    #  Внутренние методы
    # ======================

    def _generate_prime(self, bits: int, certainty: int) -> int:
        """Генерация большого вероятно простого числа."""
        attempts = 0
        while True:
            # Генерируем случайное нечетное число в диапазоне [2^(bits-1), 2^bits)
            candidate = self._random_odd_of_bit_length(bits)
            attempts += 1
            logger.debug(
                "ElGamal prime generation attempt #%d, candidate bit_length=%s",
                attempts,
                candidate.bit_length(),
            )
            if self._is_probable_prime(candidate, certainty):
                logger.info("Prime found after %d attempts (%d bits)", attempts, bits)
                return candidate

    @staticmethod
    def _random_odd_of_bit_length(bits: int) -> int:
        """Генерирует случайное нечетное число заданной битовой длины."""
        if bits < 2:
            raise ValueError("bits must be >= 2")

        # Устанавливаем старший и младший (чтобы число было нечетным) биты.
        n = secrets.randbits(bits - 2)
        n |= 1 << (bits - 2)  # старший бит
        n <<= 1
        n |= 1  # делаем нечетным
        return n

    def _is_probable_prime(self, n: int, k: int) -> bool:
        """Проверка Миллера–Рабина."""
        logger.debug("Running Miller-Rabin primality test: n_bits=%s, rounds=%s", n.bit_length(), k)
        if n < 2:
            return False
        if n in (2, 3):
            return True
        if n % 2 == 0:
            return False

        # Представляем n-1 как d * 2^s с нечетным d
        d = n - 1
        s = 0
        while d % 2 == 0:
            d //= 2
            s += 1

        for _ in range(k):
            a = self._random_in_range(2, n - 2)
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue

            is_composite = True
            for _ in range(1, s):
                x = pow(x, 2, n)
                if x == 1:
                    return False
                if x == n - 1:
                    is_composite = False
                    break

            if is_composite:
                return False

        return True

    def _find_primitive_root_fast(self, p: int) -> int:
        """Поиск первообразного корня по модулю p.

        Логика упрощена по сравнению с C#-версией: вместо полного
        факторизации p-1 используем несколько эвристик.
        Для учебных задач этого достаточно.
        """
        p_minus_1 = p - 1

        # Попробуем несколько малых кандидатов
        small_candidates = (2, 3, 5, 6, 7, 10)
        for g in small_candidates:
            if g >= p:
                continue
            if self._check_generator_candidate(g, p, p_minus_1):
                logger.info("Found small primitive root candidate g=%s for p", g)
                return g

        # Если не нашли — пробуем случайные
        for _ in range(self._MAX_PRIMITIVE_ROOT_TRIES):
            g = self._random_in_range(2, p - 2)
            if self._check_generator_candidate(g, p, p_minus_1):
                logger.info("Found random primitive root candidate g=%s for p", g)
                return g

        raise RuntimeError("Failed to find primitive root modulo p")

    @staticmethod
    def _check_generator_candidate(g: int, p: int, p_minus_1: int) -> bool:
        """Грубая проверка кандидата в генераторы."""
        # Базовые проверки: g^((p-1)/2) != 1, g^2 != 1 и т.п.
        # Без полной факторизации это не гарантирует, что g — первообразный корень,
        # но на практике для случайных p этого обычно достаточно.
        if pow(g, 2, p) == 1:
            logger.debug("Rejecting generator candidate g=%s: g^2 ≡ 1 (mod p)", g)
            return False
        if pow(g, p_minus_1 // 2, p) == 1:
            logger.debug("Rejecting generator candidate g=%s: g^((p-1)/2) ≡ 1 (mod p)", g)
            return False
        if pow(g, p_minus_1, p) != 1:
            logger.debug("Rejecting generator candidate g=%s: g^(p-1) != 1 (mod p)", g)
            return False
        logger.debug("Accepted generator candidate g=%s", g)
        return True

    @staticmethod
    def _generate_private_key(p: int) -> int:
        """Генерация закрытого ключа x в диапазоне [2, p-2]."""
        if p <= 4:
            raise ValueError("Modulus p is too small for key generation")
        x = ElGamalService._random_in_range(2, p - 2)
        logger.info("Generated ElGamal private key x (bits=%s)", x.bit_length())
        return x

    @staticmethod
    def _random_in_range(min_value: int, max_value: int) -> int:
        """Случайное число в диапазоне [min_value, max_value]."""
        if min_value > max_value:
            raise ValueError("min_value must be <= max_value")
        if min_value == max_value:
            return min_value

        # Аналог NextBigInteger из C#, но через secrets
        range_size = max_value - min_value + 1
        num_bits = range_size.bit_length()
        while True:
            candidate = secrets.randbits(num_bits)
            if candidate < range_size:
                value = min_value + candidate
                logger.debug(
                    "Generated random integer in range [%s, %s]: %s (bits=%s)",
                    min_value,
                    max_value,
                    value,
                    value.bit_length(),
                )
                return value
