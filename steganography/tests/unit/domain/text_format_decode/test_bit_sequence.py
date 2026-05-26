"""Тесты утилит работы с битовой строкой."""

from steganography.domain.text_format_decode.services.bit_sequence import (
    build_bit_sequence,
    trim_trailing_zeros,
)
from steganography.domain.common.value_objects.formatting_method import (
    FormattingMethod,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from tests.unit.factories.formatted_char_factory import container_from_bits


def test_build_bit_sequence_reproduces_source_bits() -> None:
    bits = "100000000010000001"
    chars = container_from_bits(bits)
    method = FormattingMethod(
        param=FormattingParam.SIZE, zero_value="28", one_value="29",
    )
    assert build_bit_sequence(chars, method) == bits


def test_trim_keeps_byte_alignment() -> None:
    assert trim_trailing_zeros("11110001" + "0" * 24) == "11110001"


def test_trim_all_zeros_returns_empty() -> None:
    assert trim_trailing_zeros("0000") == ""
