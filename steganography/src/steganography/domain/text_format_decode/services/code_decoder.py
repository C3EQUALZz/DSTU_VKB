"""CodeDecoder — переводит битовую строку в осмысленное сообщение."""

from math import tanh
from typing import Final

from steganography.domain.common.encodings.encoding import Encoding
from steganography.domain.common.encodings.encoding_registry import (
    EncodingRegistry,
)
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)
from steganography.domain.text_format_decode.language.russian_language_statistics import (
    RussianLanguageStatistics,
)
from steganography.domain.text_format_decode.services.bit_sequence import (
    build_bit_sequence,
    trim_trailing_zeros,
)
from steganography.domain.text_format_decode.value_objects.decoded_message import (
    DecodedMessage,
)
from steganography.domain.text_format_decode.value_objects.formatted_char import (
    FormattedChar,
)

_RU_LETTERS: Final[frozenset[str]] = frozenset(
    "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя",
)
_LATIN_LETTERS: Final[frozenset[str]] = frozenset(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
)
_PUNCT_AND_DIGITS: Final[frozenset[str]] = frozenset(
    "0123456789 \n\r\t.,;:!?-—«»\"'()/—",
)


class CodeDecoder:
    """Декодирует биты контейнера, перебирая кодировки и инверсию ролей."""

    def __init__(
        self,
        registry: EncodingRegistry,
        language: RussianLanguageStatistics,
        min_score: float,
    ) -> None:
        self._registry = registry
        self._language = language
        self._min_score = min_score

    def decode(
        self,
        chars: list[FormattedChar],
        method: FormattingMethod,
    ) -> DecodedMessage | None:
        inverted: FormattingMethod = FormattingMethod(
            param=method.param,
            zero_value=method.one_value,
            one_value=method.zero_value,
        )
        candidates: list[tuple[float, DecodedMessage]] = []
        for variant_method in (method, inverted):
            bits: str = build_bit_sequence(chars, variant_method)
            trimmed: str = trim_trailing_zeros(bits)
            if not trimmed:
                continue
            for encoding in self._registry.all():
                text: str | None = encoding.decode(trimmed)
                if text is None:
                    continue
                score: float = _meaningfulness_score(text)
                if score < self._min_score:
                    continue
                weight: float = self._confidence(text, score, encoding)
                candidates.append(
                    (
                        weight,
                        DecodedMessage(
                            method=variant_method,
                            encoding=encoding,
                            bit_sequence=trimmed,
                            message=text,
                        ),
                    ),
                )
        if not candidates:
            return None
        candidates.sort(key=lambda item: -item[0])
        return candidates[0][1]

    def _confidence(
        self, text: str, score: float, encoding: Encoding,
    ) -> float:
        length_factor: float = tanh(len(text) / 5)
        # МТК-2 при случайных 5-битных группах почти всегда выдаёт буквы —
        # принижаем её доверие, чтобы 8-битные кодировки выигрывали при
        # реальном тексте, а не на «псевдо-кириллическом шуме».
        prior: float = (
            0.5 if encoding is self._registry.mtk2 else 1.0
        )
        return score * length_factor * prior * self._language.likeness(text)


def _meaningfulness_score(text: str) -> float:
    if not text:
        return 0.0
    ru: int = sum(1 for ch in text if ch in _RU_LETTERS)
    en: int = sum(1 for ch in text if ch in _LATIN_LETTERS)
    pad: int = sum(1 for ch in text if ch in _PUNCT_AND_DIGITS)
    letters: int = max(ru, en)
    return (letters + 0.5 * pad) / len(text)
