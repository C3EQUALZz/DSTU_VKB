"""ГОСТ Р 34.10-94 digital signature service."""

import hashlib
import logging
import secrets
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService,
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Gost341094Parameters:
    """Параметры схемы ГОСТ Р 34.10-94."""

    p: int
    q: int
    a: int


@dataclass(frozen=True, slots=True)
class Gost341094PrivateKey:
    """Закрытый ключ ГОСТ Р 34.10-94."""

    x: int


@dataclass(frozen=True, slots=True)
class Gost341094PublicKey:
    """Открытый ключ ГОСТ Р 34.10-94."""

    y: int


@dataclass(frozen=True, slots=True)
class Gost341094KeyPair:
    """Пара ключей ГОСТ Р 34.10-94."""

    parameters: Gost341094Parameters
    private_key: Gost341094PrivateKey
    public_key: Gost341094PublicKey


@dataclass(frozen=True, slots=True)
class Gost341094Signature:
    """Цифровая подпись ГОСТ Р 34.10-94."""

    r: int
    s: int


class Gost341094Service(DomainService):
    """Сервис для работы с ЭЦП по ГОСТ Р 34.10-94."""

    _DEFAULT_KEY_SIZE: Final[int] = 512
    _Q_BIT_LENGTH: Final[int] = 256

    def __init__(
        self,
        prime_number_service: PrimeNumberService,
        modular_arithmetic_service: ModularArithmeticService,
    ) -> None:
        """Инициализация сервиса ГОСТ Р 34.10-94.

        Args:
            prime_number_service: Сервис для генерации простых чисел
            modular_arithmetic_service: Сервис для модульной арифметики
        """
        super().__init__()
        self._prime_service: Final[PrimeNumberService] = prime_number_service
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service
        logger.info("Initialized Gost341094Service")

    def generate_parameters_and_keys(
        self,
        key_size: int = 512,
    ) -> Gost341094KeyPair:
        """Генерация параметров и ключей ГОСТ Р 34.10-94.

        Args:
            key_size: Размер ключа в битах (512 или 1024)

        Returns:
            Пара ключей с параметрами схемы
        """
        if key_size not in (512, 1024):
            raise ValueError("Недопустимый размер ключа. Используйте 512 или 1024 бит.")

        logger.info("=== Генерация параметров ГОСТ Р 34.10-94 ===")
        logger.info("Размер ключа: %s бит", key_size)

        # 1. Генерация простого числа q (256 бит)
        logger.info("[1] Генерация простого числа q (%s бит)...", self._Q_BIT_LENGTH)
        q = self._prime_service.generate_large_prime(self._Q_BIT_LENGTH)
        logger.info("q (%s бит): %s", q.bit_length(), q)

        # 2. Генерация простого числа p = k*q + 1
        logger.info("[2] Генерация простого числа p = k*q + 1...")
        k_bits = key_size - self._Q_BIT_LENGTH
        p, attempts = self._generate_p_from_q(q, k_bits)
        logger.info("Найдено p (%s бит) за %s попыток", p.bit_length(), attempts)

        # 3. Поиск генератора a
        logger.info("[3] Поиск генератора a...")
        a = self._find_generator(p, q)
        logger.info("Найден генератор a: %s", a)

        # 4. Генерация ключей
        logger.info("[4] Генерация ключей...")
        x = self._generate_random_in_range(2, q - 1)
        y = self._modular_arithmetic.mod_pow(a, x, p)
        logger.info("Закрытый ключ x: %s", x)
        logger.info("Открытый ключ y: %s", y)

        parameters = Gost341094Parameters(p=p, q=q, a=a)
        private_key = Gost341094PrivateKey(x=x)
        public_key = Gost341094PublicKey(y=y)

        logger.info("=== Параметры ГОСТ Р 34.10-94 ===")
        logger.info("p (%s бит): %s", p.bit_length(), p)
        logger.info("q (%s бит): %s", q.bit_length(), q)
        logger.info("a: %s", a)
        logger.info("Открытый ключ y: %s", y)
        logger.info("q делитель (p-1): %s", (p - 1) % q == 0)
        logger.info("a^q mod p = 1: %s", self._modular_arithmetic.mod_pow(a, q, p) == 1)

        return Gost341094KeyPair(
            parameters=parameters,
            private_key=private_key,
            public_key=public_key,
        )

    def _generate_p_from_q(self, q: int, k_bits: int) -> tuple[int, int]:
        """Генерация простого числа p = k*q + 1.

        Args:
            q: Простое число q
            k_bits: Размер k в битах

        Returns:
            (p, количество попыток)
        """
        attempts = 0
        while True:
            attempts += 1
            k = self._generate_random_big_integer(k_bits)
            p = k * q + 1
            logger.debug("Попытка %s: генерация p = k*q + 1, k_bits=%s", attempts, k_bits)

            if self._prime_service.miller_rabin_test(p, k=20):
                return p, attempts

    def _find_generator(self, p: int, q: int) -> int:
        """Поиск генератора a по модулю p.

        Генератор должен удовлетворять: a^q mod p = 1 и a != 1.

        Args:
            p: Простое число p
            q: Простое число q (делитель p-1)

        Returns:
            Генератор a

        Raises:
            RuntimeError: Если генератор не найден за 100 попыток
        """
        p_minus_1 = p - 1
        for i in range(100):
            h = self._generate_random_in_range(2, p - 2)
            g = self._modular_arithmetic.mod_pow(h, p_minus_1 // q, p)
            if g != 1 and self._modular_arithmetic.mod_pow(g, q, p) == 1:
                logger.debug("Найден генератор за %s попыток", i + 1)
                return g

        raise RuntimeError("Генератор не найден за 100 попыток")

    def compute_hash(self, data: bytes, q: int) -> int:
        """Вычисление хеша данных по ГОСТ Р 34.10-94.

        Используется SHA-256, результат берётся по модулю q.

        Args:
            data: Данные для хеширования
            q: Модуль q

        Returns:
            Хеш по модулю q
        """
        logger.info("Вычисление хеша файла (SHA-256)...")
        hash_bytes = hashlib.sha256(data).digest()
        hash_int = int.from_bytes(hash_bytes, byteorder="big", signed=False)
        hash_mod_q = hash_int % q
        logger.info("Полученный хеш: %s", hash_mod_q)
        logger.debug("SHA-256 (hex): %s", hash_bytes.hex())
        return hash_mod_q

    def create_signature(
        self,
        hash_value: int,
        parameters: Gost341094Parameters,
        private_key: Gost341094PrivateKey,
    ) -> Gost341094Signature:
        """Создание цифровой подписи ГОСТ Р 34.10-94.

        Args:
            hash_value: Хеш документа (по модулю q)
            parameters: Параметры схемы
            private_key: Закрытый ключ

        Returns:
            Цифровая подпись (r, s)
        """
        if hash_value == 0:
            hash_value = 1
            logger.debug("Хеш равен 0, заменён на 1")

        logger.info("--- Процесс создания подписи ---")
        p = parameters.p
        q = parameters.q
        a = parameters.a
        x = private_key.x

        attempts = 0
        while True:
            attempts += 1
            k = self._generate_random_in_range(2, q - 1)
            logger.debug("Попытка %s:", attempts)
            logger.debug("  Сгенерирован k: %s", k)

            r = self._modular_arithmetic.mod_pow(a, k, p) % q
            logger.debug("  Вычислено r: %s", r)

            s = (x * r + k * hash_value) % q
            logger.debug("  Вычислено s: %s", s)

            if r != 0 and s != 0:
                logger.info("Подпись создана за %s попыток", attempts)
                return Gost341094Signature(r=r, s=s)

    def verify_signature(
        self,
        hash_value: int,
        signature: Gost341094Signature,
        parameters: Gost341094Parameters,
        public_key: Gost341094PublicKey,
    ) -> bool:
        """Проверка цифровой подписи ГОСТ Р 34.10-94.

        Args:
            hash_value: Хеш документа (по модулю q)
            signature: Цифровая подпись
            parameters: Параметры схемы
            public_key: Открытый ключ

        Returns:
            True если подпись валидна, False иначе
        """
        logger.info("--- Детали проверки подписи ---")
        q = parameters.q
        r = signature.r
        s = signature.s

        logger.info("Проверка условий:")
        logger.info("1. 0 < r < q: %s", r > 0 and r < q)
        logger.info("2. 0 < s < q: %s", s > 0 and s < q)

        if r <= 0 or r >= q or s <= 0 or s >= q:
            logger.info("Подпись невалидна: нарушены условия на r и s")
            return False

        # v = hash^(q-2) mod q
        v = self._modular_arithmetic.mod_pow(hash_value, q - 2, q)
        logger.info("Вычислено v = hash^(q-2) mod q: %s", v)

        # z1 = s*v mod q
        z1 = (s * v) % q
        # z2 = (q - r)*v mod q
        z2 = ((q - r) * v) % q
        logger.info("Вычислены:")
        logger.info("  z1 = %s", z1)
        logger.info("  z2 = %s", z2)

        # u = (a^z1 * y^z2 mod p) mod q
        a_z1 = self._modular_arithmetic.mod_pow(parameters.a, z1, parameters.p)
        y_z2 = self._modular_arithmetic.mod_pow(public_key.y, z2, parameters.p)
        u = (a_z1 * y_z2) % parameters.p % q
        logger.info("Вычислено u = (a^z1 * y^z2 mod p) mod q: %s", u)

        is_valid = u == r
        logger.info("Результат проверки: %s", "ВАЛИДНА" if is_valid else "НЕВАЛИДНА")
        return is_valid

    def _generate_random_big_integer(self, bit_length: int) -> int:
        """Генерация случайного большого числа заданной битовой длины.

        Args:
            bit_length: Длина в битах

        Returns:
            Случайное число
        """
        num_bytes = (bit_length + 7) // 8
        random_bytes = secrets.token_bytes(num_bytes)

        # Маскируем последний байт для правильной битовой длины
        if bit_length % 8 != 0:
            mask = 0xFF >> (8 - (bit_length % 8))
            random_bytes = bytearray(random_bytes)
            random_bytes[-1] &= mask
            random_bytes = bytes(random_bytes)

        candidate = int.from_bytes(random_bytes, byteorder="big", signed=False)

        # Устанавливаем старший бит
        max_value = 1 << bit_length
        if candidate >= max_value:
            candidate %= max_value

        # Устанавливаем старший бит для правильной длины
        if candidate < (1 << (bit_length - 1)):
            candidate |= 1 << (bit_length - 1)

        return candidate

    def _generate_random_in_range(self, min_value: int, max_value: int) -> int:
        """Генерация случайного числа в диапазоне [min_value, max_value).

        Args:
            min_value: Минимальное значение (включительно)
            max_value: Максимальное значение (исключительно)

        Returns:
            Случайное число в диапазоне
        """
        if min_value >= max_value:
            raise ValueError("min_value must be < max_value")

        range_size = max_value - min_value
        num_bits = range_size.bit_length()
        num_bytes = (num_bits + 7) // 8

        while True:
            random_bytes = secrets.token_bytes(num_bytes)
            candidate = int.from_bytes(random_bytes, byteorder="big", signed=False)
            candidate = min_value + (candidate % range_size)

            if min_value <= candidate < max_value:
                return candidate

    # ==================
    #  Key I/O helpers
    # ==================

    @staticmethod
    def save_parameters_and_keys(
        key_pair: Gost341094KeyPair,
        parameters_file: Path,
        private_key_file: Path,
        public_key_file: Path,
    ) -> None:
        """Сохранение параметров и ключей в файлы.

        Args:
            key_pair: Пара ключей с параметрами
            parameters_file: Путь к файлу параметров
            private_key_file: Путь к файлу закрытого ключа
            public_key_file: Путь к файлу открытого ключа
        """
        logger.info("Сохранение параметров и ключей ГОСТ Р 34.10-94...")

        # Сохранение параметров (p, q, a)
        parameters_file.parent.mkdir(parents=True, exist_ok=True)
        with parameters_file.open("w", encoding="utf-8") as f:
            f.write(f"{key_pair.parameters.p}\n")
            f.write(f"{key_pair.parameters.q}\n")
            f.write(f"{key_pair.parameters.a}\n")
        logger.info("Параметры сохранены в: %s", parameters_file)

        # Сохранение закрытого ключа (x)
        private_key_file.parent.mkdir(parents=True, exist_ok=True)
        with private_key_file.open("w", encoding="utf-8") as f:
            f.write(f"{key_pair.private_key.x}\n")
        logger.info("Закрытый ключ сохранён в: %s", private_key_file)

        # Сохранение открытого ключа (y)
        public_key_file.parent.mkdir(parents=True, exist_ok=True)
        with public_key_file.open("w", encoding="utf-8") as f:
            f.write(f"{key_pair.public_key.y}\n")
        logger.info("Открытый ключ сохранён в: %s", public_key_file)

    @staticmethod
    def load_parameters(file_path: Path) -> Gost341094Parameters:
        """Загрузка параметров из файла.

        Args:
            file_path: Путь к файлу параметров

        Returns:
            Параметры схемы
        """
        logger.info("Загрузка параметров из файла: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл параметров не найден: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 3:
            raise ValueError("Неверный формат файла параметров: ожидается 3 строки (p, q, a)")

        p = int(lines[0])
        q = int(lines[1])
        a = int(lines[2])

        logger.info("Параметры загружены: p (%s бит), q (%s бит), a", p.bit_length(), q.bit_length())
        return Gost341094Parameters(p=p, q=q, a=a)

    @staticmethod
    def load_private_key(file_path: Path) -> Gost341094PrivateKey:
        """Загрузка закрытого ключа из файла.

        Args:
            file_path: Путь к файлу закрытого ключа

        Returns:
            Закрытый ключ
        """
        logger.info("Загрузка закрытого ключа из файла: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл закрытого ключа не найден: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 1:
            raise ValueError("Неверный формат файла закрытого ключа: ожидается 1 строка (x)")

        x = int(lines[0])
        logger.info("Закрытый ключ загружен: x")
        return Gost341094PrivateKey(x=x)

    @staticmethod
    def load_public_key(file_path: Path) -> Gost341094PublicKey:
        """Загрузка открытого ключа из файла.

        Args:
            file_path: Путь к файлу открытого ключа

        Returns:
            Открытый ключ
        """
        logger.info("Загрузка открытого ключа из файла: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл открытого ключа не найден: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 1:
            raise ValueError("Неверный формат файла открытого ключа: ожидается 1 строка (y)")

        y = int(lines[0])
        logger.info("Открытый ключ загружен: y")
        return Gost341094PublicKey(y=y)

    @staticmethod
    def save_signature(signature: Gost341094Signature, q: int, file_path: Path) -> None:
        """Сохранение подписи в файл.

        Формат: q\nr\ns

        Args:
            signature: Цифровая подпись
            q: Параметр q (для совместимости с форматом из C#)
            file_path: Путь к файлу подписи
        """
        logger.info("Сохранение подписи в файл: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"{q}\n")
            f.write(f"{signature.r}\n")
            f.write(f"{signature.s}\n")

        logger.info("Подпись сохранена: r=%s, s=%s", signature.r, signature.s)

    @staticmethod
    def load_signature(file_path: Path) -> tuple[int, Gost341094Signature]:
        """Загрузка подписи из файла.

        Формат: q\nr\ns

        Args:
            file_path: Путь к файлу подписи

        Returns:
            (q, signature)
        """
        logger.info("Загрузка подписи из файла: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Файл подписи не найден: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 3:
            raise ValueError("Неверный формат файла подписи: ожидается 3 строки (q, r, s)")

        q = int(lines[0])
        r = int(lines[1])
        s = int(lines[2])

        logger.info("Подпись загружена: q=%s, r=%s, s=%s", q, r, s)
        return q, Gost341094Signature(r=r, s=s)

