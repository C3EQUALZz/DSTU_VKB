"""ГОСТ Р 34.11-94 hash service."""

import logging
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService

logger: Final[logging.Logger] = logging.getLogger(__name__)


class Gost341194HashService(DomainService):
    """Сервис вычисления хеша по ГОСТ Р 34.11-94.

    Реализация использует начальное значение h0 = 0^256 и тестовые
    параметры подстановок из RFC 5831. Выходной размер хеша - 256 бит.
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
        """Вычислить 256-битный хеш по ГОСТ Р 34.11-94."""
        logger.info("Вычисление хеша файла (ГОСТ Р 34.11-94)...")

        hash_value = bytes(self._BLOCK_SIZE)
        checksum = bytes(self._BLOCK_SIZE)
        unprocessed = data
        processed_bits = 0

        while len(unprocessed) > self._BLOCK_SIZE:
            block = unprocessed[-self._BLOCK_SIZE :]
            unprocessed = unprocessed[: -self._BLOCK_SIZE]

            hash_value = self._step_hash(block, hash_value)
            checksum = self._add_mod_256(checksum, block)
            processed_bits += self._BLOCK_SIZE * 8

        length = (processed_bits + len(unprocessed) * 8).to_bytes(
            self._BLOCK_SIZE,
            byteorder="big",
        )
        final_block = bytes(self._BLOCK_SIZE - len(unprocessed)) + unprocessed
        checksum = self._add_mod_256(checksum, final_block)

        hash_value = self._step_hash(final_block, hash_value)
        hash_value = self._step_hash(length, hash_value)
        hash_value = self._step_hash(checksum, hash_value)

        logger.debug("ГОСТ Р 34.11-94 hash (hex): %s", hash_value.hex())
        return hash_value

    def digest_int(self, data: bytes) -> int:
        """Вычислить хеш и представить его как неотрицательное число."""
        return int.from_bytes(self.digest(data), byteorder="big", signed=False)

    @classmethod
    def _step_hash(cls, message_block: bytes, hash_value: bytes) -> bytes:
        keys = cls._generate_keys(hash_value, message_block)

        encrypted_parts = []
        for index, key in enumerate(keys):
            end = cls._BLOCK_SIZE - index * cls._WORD64_SIZE
            start = end - cls._WORD64_SIZE
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
        return cls._psi_power(mixed, 61)

    @classmethod
    def _generate_keys(
        cls,
        hash_value: bytes,
        message_block: bytes,
    ) -> list[bytes]:
        u = hash_value
        v = message_block
        keys = [cls._permutation_p(cls._xor_bytes(u, v))]

        for index in range(1, 4):
            u = cls._xor_bytes(cls._transform_a(u), cls._C[index])
            v = cls._transform_a(cls._transform_a(v))
            keys.append(cls._permutation_p(cls._xor_bytes(u, v)))

        return keys

    @classmethod
    def _encrypt_block(cls, block: bytes, key: bytes) -> bytes:
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

        return n2.to_bytes(4, byteorder="big") + n1.to_bytes(
            4,
            byteorder="big",
        )

    @classmethod
    def _cipher_round(cls, value: int) -> int:
        substituted = 0
        for index, sbox in enumerate(cls._SBOX):
            nibble = (value >> (4 * index)) & 0x0F
            substituted |= sbox[nibble] << (4 * index)

        return cls._rotate_left_32(substituted, 11)

    @staticmethod
    def _rotate_left_32(value: int, shift: int) -> int:
        return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF

    @classmethod
    def _transform_a(cls, value: bytes) -> bytes:
        x4 = value[:8]
        x3 = value[8:16]
        x2 = value[16:24]
        x1 = value[24:32]
        return cls._xor_bytes(x1, x2) + x4 + x3 + x2

    @classmethod
    def _permutation_p(cls, value: bytes) -> bytes:
        return bytes(value[index] for index in cls._P_PERMUTATION)

    @classmethod
    def _psi_power(cls, value: bytes, power: int) -> bytes:
        for _ in range(power):
            value = cls._psi(value)
        return value

    @classmethod
    def _psi(cls, value: bytes) -> bytes:
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
        result = (
            int.from_bytes(left, "big") + int.from_bytes(right, "big")
        ) % cls._MOD_256
        return result.to_bytes(cls._BLOCK_SIZE, byteorder="big")

    @staticmethod
    def _xor_bytes(left: bytes, right: bytes) -> bytes:
        return bytes(
            left_byte ^ right_byte
            for left_byte, right_byte in zip(left, right, strict=False)
        )
