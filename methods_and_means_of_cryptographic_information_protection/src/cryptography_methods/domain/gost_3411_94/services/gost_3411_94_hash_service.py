# ruff: noqa: RUF001, RUF002
"""Сервис вычисления хеша по ГОСТ Р 34.11-94.

Модуль содержит прикладную реализацию 256-битной хеш-функции
ГОСТ Р 34.11-94. Код оставлен самодостаточным: все преобразования,
таблицы подстановок, перестановки и вспомогательные операции описаны
внутри сервиса, чтобы его можно было использовать из схемы подписи
ГОСТ Р 34.10-94 без дополнительных зависимостей.
"""

import logging
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class Gost341194HashService(DomainService):
    """Сервис вычисления хеша по ГОСТ Р 34.11-94.

    Сервис принимает произвольную последовательность байтов и возвращает
    32-байтовый дайджест. Внутри данные обрабатываются блоками по 256 бит:
    для каждого блока выполняется шаг сжатия, отдельно накапливается
    контрольная сумма всех блоков по модулю 2^256, а в конце в состояние
    добавляются блок длины сообщения и блок контрольной суммы.

    Реализация использует нулевое начальное значение ``h0 = 0^256`` и
    тестовые параметры подстановок из RFC 5831. Порядок байтов во всех
    целочисленных преобразованиях выбран ``big-endian`` и согласован со
    существующей реализацией подписи ГОСТ Р 34.10-94 в проекте.
    """

    _BLOCK_SIZE: Final[int] = 32
    _WORD64_SIZE: Final[int] = 8
    _MOD_256: Final[int] = 1 << 256

    _P_PERMUTATION: Final[tuple[int, ...]] = (
        0,
        8,
        16,
        24,
        1,
        9,
        17,
        25,
        2,
        10,
        18,
        26,
        3,
        11,
        19,
        27,
        4,
        12,
        20,
        28,
        5,
        13,
        21,
        29,
        6,
        14,
        22,
        30,
        7,
        15,
        23,
        31,
    )

    _C: Final[tuple[bytes, bytes, bytes, bytes]] = (
        bytes(_BLOCK_SIZE),
        bytes(_BLOCK_SIZE),
        bytes.fromhex(
            "FF00FFFF000000FFFF0000FF00FFFF0000FF00FF00FF00FFFF00FF00FF00FF00",
        ),
        bytes(_BLOCK_SIZE),
    )

    _SBOX: Final[tuple[tuple[int, ...], ...]] = (
        (
            0x4,
            0xA,
            0x9,
            0x2,
            0xD,
            0x8,
            0x0,
            0xE,
            0x6,
            0xB,
            0x1,
            0xC,
            0x7,
            0xF,
            0x5,
            0x3,
        ),
        (
            0xE,
            0xB,
            0x4,
            0xC,
            0x6,
            0xD,
            0xF,
            0xA,
            0x2,
            0x3,
            0x8,
            0x1,
            0x0,
            0x7,
            0x5,
            0x9,
        ),
        (
            0x5,
            0x8,
            0x1,
            0xD,
            0xA,
            0x3,
            0x4,
            0x2,
            0xE,
            0xF,
            0xC,
            0x7,
            0x6,
            0x0,
            0x9,
            0xB,
        ),
        (
            0x7,
            0xD,
            0xA,
            0x1,
            0x0,
            0x8,
            0x9,
            0xF,
            0xE,
            0x4,
            0x6,
            0xC,
            0xB,
            0x2,
            0x5,
            0x3,
        ),
        (
            0x6,
            0xC,
            0x7,
            0x1,
            0x5,
            0xF,
            0xD,
            0x8,
            0x4,
            0xA,
            0x9,
            0xE,
            0x0,
            0x3,
            0xB,
            0x2,
        ),
        (
            0x4,
            0xB,
            0xA,
            0x0,
            0x7,
            0x2,
            0x1,
            0xD,
            0x3,
            0x6,
            0x8,
            0x5,
            0x9,
            0xC,
            0xF,
            0xE,
        ),
        (
            0xD,
            0xB,
            0x4,
            0x1,
            0x3,
            0xF,
            0x5,
            0x9,
            0x0,
            0xA,
            0xE,
            0x7,
            0x6,
            0x8,
            0x2,
            0xC,
        ),
        (
            0x1,
            0xF,
            0xD,
            0x0,
            0x5,
            0x7,
            0xA,
            0x4,
            0x9,
            0x2,
            0x3,
            0xE,
            0x6,
            0xB,
            0x8,
            0xC,
        ),
    )

    def digest(self, data: bytes) -> bytes:
        """Вычислить 256-битный хеш по ГОСТ Р 34.11-94.

        Метод реализует полный цикл хеширования:

        * инициализирует состояние хеша и контрольную сумму нулевыми
          256-битными блоками;
        * обрабатывает вход справа налево полными 32-байтовыми блоками;
        * дополняет последний неполный блок нулями слева до 32 байт;
        * добавляет в цепочку сжатия блок длины исходного сообщения;
        * добавляет в цепочку сжатия накопленную контрольную сумму.

        Args:
            data: Исходные байты сообщения. Метод не выполняет кодирование
                строк и ожидает уже подготовленный ``bytes``.

        Returns:
            32 байта хеша. Для текстового представления используйте
            ``digest(data).hex()``, а для числового - ``digest_int``.
        """
        logger.info(
            "Начато вычисление хеша ГОСТ Р 34.11-94: размер данных %s байт",
            len(data),
        )

        hash_value = bytes(self._BLOCK_SIZE)
        checksum = bytes(self._BLOCK_SIZE)
        unprocessed = data
        processed_bits = 0
        processed_blocks = 0

        logger.info(
            "Инициализированы h0 и контрольная сумма: %s байт каждый",
            self._BLOCK_SIZE,
        )

        while len(unprocessed) > self._BLOCK_SIZE:
            processed_blocks += 1
            block = unprocessed[-self._BLOCK_SIZE :]
            unprocessed = unprocessed[: -self._BLOCK_SIZE]

            logger.info(
                "Обработка полного блока #%s с конца сообщения: %s байт",
                processed_blocks,
                len(block),
            )
            hash_value = self._step_hash(block, hash_value)
            checksum = self._add_mod_256(checksum, block)
            processed_bits += self._BLOCK_SIZE * 8

        logger.info(
            "Полных блоков до финального блока обработано: %s",
            processed_blocks,
        )
        length = (processed_bits + len(unprocessed) * 8).to_bytes(
            self._BLOCK_SIZE,
            byteorder="big",
        )
        final_block = bytes(self._BLOCK_SIZE - len(unprocessed)) + unprocessed
        logger.info(
            "Подготовлен финальный блок: остаток %s байт, дополнение %s байт",
            len(unprocessed),
            self._BLOCK_SIZE - len(unprocessed),
        )
        checksum = self._add_mod_256(checksum, final_block)

        logger.info("Выполняется шаг сжатия для финального блока сообщения")
        hash_value = self._step_hash(final_block, hash_value)
        logger.info(
            "Выполняется шаг сжатия для блока длины сообщения: %s бит",
            processed_bits + len(unprocessed) * 8,
        )
        hash_value = self._step_hash(length, hash_value)
        logger.info("Выполняется шаг сжатия для контрольной суммы сообщения")
        hash_value = self._step_hash(checksum, hash_value)

        logger.info("ГОСТ Р 34.11-94 hash (hex): %s", hash_value.hex())
        return hash_value

    def digest_int(self, data: bytes) -> int:
        """Вычислить хеш и представить его как неотрицательное число.

        Метод является удобной обёрткой над ``digest`` для алгоритмов,
        которым нужен числовой образ хеша. Например, ГОСТ Р 34.10-94
        дополнительно приводит это число по модулю ``q``.

        Args:
            data: Исходные байты сообщения.

        Returns:
            Неотрицательное целое число, полученное из 32 байт дайджеста в
            порядке ``big-endian``.
        """
        logger.info(
            "Запрошено числовое представление хеша ГОСТ Р 34.11-94",
        )
        digest = self.digest(data)
        digest_as_int = int.from_bytes(digest, byteorder="big", signed=False)
        logger.info(
            "Хеш ГОСТ Р 34.11-94 преобразован в число: bit_length=%s",
            digest_as_int.bit_length(),
        )
        return digest_as_int

    @classmethod
    def _step_hash(cls, message_block: bytes, hash_value: bytes) -> bytes:
        """Выполнить один шаг функции сжатия для 256-битного блока.

        Шаг сжатия строит четыре 256-битных ключа из текущего состояния
        ``hash_value`` и блока сообщения ``message_block``. Затем четыре
        64-битные части состояния шифруются блочным преобразованием,
        объединяются в 256-битное значение и проходят через линейное
        преобразование ``psi`` с примешиванием блока и прошлого состояния.

        Args:
            message_block: Очередной 32-байтовый блок сообщения.
            hash_value: Текущее 32-байтовое состояние цепочки хеширования.

        Returns:
            Новое 32-байтовое состояние хеша.
        """
        logger.info(
            "Старт шага сжатия ГОСТ Р 34.11-94: block=%s байт, hash=%s байт",
            len(message_block),
            len(hash_value),
        )
        keys = cls._generate_keys(hash_value, message_block)

        encrypted_parts = []
        for index, key in enumerate(keys):
            end = cls._BLOCK_SIZE - index * cls._WORD64_SIZE
            start = end - cls._WORD64_SIZE
            logger.info(
                "Шифрование 64-битной части #%s текущего состояния",
                index + 1,
            )
            encrypted_parts.append(
                cls._encrypt_block(hash_value[start:end], key),
            )

        encrypted = b"".join(reversed(encrypted_parts))
        mixed = cls._xor_bytes(
            message_block,
            cls._psi_power(encrypted, 12),
        )
        mixed = cls._psi(mixed)
        mixed = cls._xor_bytes(hash_value, mixed)
        result = cls._psi_power(mixed, 61)
        logger.info("Шаг сжатия ГОСТ Р 34.11-94 завершён")
        return result

    @classmethod
    def _generate_keys(
        cls,
        hash_value: bytes,
        message_block: bytes,
    ) -> list[bytes]:
        """Сгенерировать четыре ключа для внутреннего блочного шифра.

        Ключи строятся из двух 256-битных регистров ``u`` и ``v``. Первый
        ключ получается перестановкой ``P(u xor v)``. Для следующих ключей
        ``u`` преобразуется функцией ``A`` и смешивается с константой ``C``,
        а ``v`` дважды преобразуется функцией ``A``. После этого снова
        применяется ``P(u xor v)``.

        Args:
            hash_value: Текущее состояние хеша, используемое как регистр
                ``u``.
            message_block: Блок сообщения, используемый как регистр ``v``.

        Returns:
            Список из четырёх 32-байтовых ключей.
        """
        logger.info("Генерация ключей функции сжатия ГОСТ Р 34.11-94")
        u = hash_value
        v = message_block
        keys = [cls._permutation_p(cls._xor_bytes(u, v))]
        logger.info("Сгенерирован ключ K1")

        for index in range(1, 4):
            u = cls._xor_bytes(cls._transform_a(u), cls._C[index])
            v = cls._transform_a(cls._transform_a(v))
            keys.append(cls._permutation_p(cls._xor_bytes(u, v)))
            logger.info("Сгенерирован ключ K%s", index + 1)

        return keys

    @classmethod
    def _encrypt_block(cls, block: bytes, key: bytes) -> bytes:
        """Зашифровать 64-битный блок внутренним ГОСТ-подобным шифром.

        В ГОСТ Р 34.11-94 функция сжатия использует блочное шифрование
        64-битных фрагментов состояния на 256-битных ключах. Здесь ключ
        разбивается на восемь 32-битных слов, а блок - на две 32-битные
        половины ``n1`` и ``n2``. Далее выполняются 32 раунда сети Фейстеля
        с расписанием ключей ``7..0`` три раза и ``0..7`` один раз.

        Args:
            block: 8-байтовая часть текущего состояния хеша.
            key: 32-байтовый ключ, полученный в ``_generate_keys``.

        Returns:
            8-байтовый зашифрованный фрагмент состояния.
        """
        logger.info(
            "Старт внутреннего шифрования блока: block=%s байт, key=%s байт",
            len(block),
            len(key),
        )
        key_words = [
            int.from_bytes(key[index : index + 4], byteorder="big")
            for index in range(0, cls._BLOCK_SIZE, 4)
        ]

        n1 = int.from_bytes(block[:4], byteorder="big")
        n2 = int.from_bytes(block[4:], byteorder="big")
        key_schedule = list(range(7, -1, -1)) * 3 + list(range(8))

        for key_index in key_schedule:
            n1, n2 = (
                n2,
                n1
                ^ cls._cipher_round((n2 + key_words[key_index]) & 0xFFFFFFFF),
            )

        result = n2.to_bytes(4, byteorder="big") + n1.to_bytes(
            4,
            byteorder="big",
        )
        logger.info("Внутреннее шифрование 64-битного блока завершено")
        return result

    @classmethod
    def _cipher_round(cls, value: int) -> int:
        """Выполнить раундовую замену и циклический сдвиг.

        32-битное значение разбивается на восемь 4-битных частей. Каждая
        часть заменяется через соответствующую строку таблицы ``_SBOX``.
        После сборки результата выполняется циклический сдвиг влево на
        11 бит.

        Args:
            value: 32-битное значение после сложения половины блока с
                раундовым словом ключа.

        Returns:
            32-битный результат раундовой функции.
        """
        substituted = 0
        for index, sbox in enumerate(cls._SBOX):
            nibble = (value >> (4 * index)) & 0x0F
            substituted |= sbox[nibble] << (4 * index)

        return cls._rotate_left_32(substituted, 11)

    @staticmethod
    def _rotate_left_32(value: int, shift: int) -> int:
        """Циклически сдвинуть 32-битное значение влево.

        Args:
            value: Исходное 32-битное значение.
            shift: Количество бит для циклического сдвига.

        Returns:
            Значение после сдвига, обрезанное маской ``0xFFFFFFFF``.
        """
        return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

    @classmethod
    def _transform_a(cls, value: bytes) -> bytes:
        """Применить линейное преобразование ``A`` к 256-битному значению.

        Значение рассматривается как четыре 64-битных слова ``x4, x3, x2,
        x1``. Результатом является ``(x1 xor x2) || x4 || x3 || x2``.
        Преобразование используется при генерации ключей функции сжатия.

        Args:
            value: 32-байтовое значение.

        Returns:
            32 байта после преобразования ``A``.
        """
        x4 = value[:8]
        x3 = value[8:16]
        x2 = value[16:24]
        x1 = value[24:32]
        return cls._xor_bytes(x1, x2) + x4 + x3 + x2

    @classmethod
    def _permutation_p(cls, value: bytes) -> bytes:
        """Применить перестановку байтов ``P``.

        Перестановка меняет порядок 32 байтов по таблице
        ``_P_PERMUTATION``. В алгоритме она превращает результат
        ``u xor v`` в очередной 256-битный ключ для внутреннего шифра.

        Args:
            value: 32-байтовое значение для перестановки.

        Returns:
            32 байта в переставленном порядке.
        """
        return bytes(value[index] for index in cls._P_PERMUTATION)

    @classmethod
    def _psi_power(cls, value: bytes, power: int) -> bytes:
        """Применить преобразование ``psi`` заданное количество раз.

        Args:
            value: 32-байтовое значение.
            power: Сколько раз последовательно выполнить ``_psi``.

        Returns:
            32 байта после ``power`` применений линейного преобразования.
        """
        logger.info("Применение преобразования psi^%s", power)
        for _ in range(power):
            value = cls._psi(value)
        logger.info("Преобразование psi^%s завершено", power)
        return value

    @classmethod
    def _psi(cls, value: bytes) -> bytes:
        """Выполнить одно линейное преобразование ``psi``.

        Вход разбивается на шестнадцать 16-битных слов. Новое первое слово
        вычисляется как XOR слов с индексами 15, 14, 13, 12, 3 и 0, после
        чего остальные слова сдвигаются вправо на одну позицию.

        Args:
            value: 32-байтовое значение.

        Returns:
            32 байта после одного шага ``psi``.
        """
        words = [
            int.from_bytes(value[index : index + 2], byteorder="big")
            for index in range(0, cls._BLOCK_SIZE, 2)
        ]
        first_word = (
            words[15] ^ words[14] ^ words[13] ^ words[12] ^ words[3] ^ words[0]
        )
        return b"".join(
            word.to_bytes(2, byteorder="big")
            for word in [first_word, *words[:15]]
        )

    @classmethod
    def _add_mod_256(cls, left: bytes, right: bytes) -> bytes:
        """Сложить два 256-битных значения по модулю 2^256.

        Операция используется для накопления контрольной суммы сообщения.
        Оба операнда интерпретируются как беззнаковые числа в порядке
        ``big-endian``.

        Args:
            left: Первый 32-байтовый операнд.
            right: Второй 32-байтовый операнд.

        Returns:
            32-байтовая сумма ``(left + right) mod 2^256``.
        """
        result = (
            int.from_bytes(left, "big") + int.from_bytes(right, "big")
        ) % cls._MOD_256
        logger.info("Контрольная сумма обновлена по модулю 2^256")
        return result.to_bytes(cls._BLOCK_SIZE, byteorder="big")

    @staticmethod
    def _xor_bytes(left: bytes, right: bytes) -> bytes:
        """Выполнить побайтовый XOR двух последовательностей.

        Args:
            left: Левая последовательность байтов.
            right: Правая последовательность байтов.

        Returns:
            Результат ``left[i] xor right[i]`` для каждой пары байтов.
            Длина результата равна длине более короткого аргумента,
            что соответствует поведению ``zip``.
        """
        return bytes(
            left_byte ^ right_byte
            for left_byte, right_byte in zip(left, right, strict=False)
        )
