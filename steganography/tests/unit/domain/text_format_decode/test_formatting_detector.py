"""Тесты детектора метода форматирования."""

from steganography.domain.text_format_decode.services.formatting_detector import (
    FormattingDetector,
)
from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from tests.unit.factories.formatted_char_factory import (
    container_from_bits,
    uniform_container,
)


def test_picks_size_param_with_two_values(
    formatting_detector: FormattingDetector,
) -> None:
    chars = container_from_bits("00010001" * 4)
    method = formatting_detector.detect(chars)
    assert method is not None
    assert method.param is FormattingParam.SIZE
    assert method.zero_value == "28"
    assert method.one_value == "29"


def test_returns_none_for_uniform_formatting(
    formatting_detector: FormattingDetector,
) -> None:
    assert formatting_detector.detect(uniform_container(20)) is None


def test_more_frequent_value_is_zero(
    formatting_detector: FormattingDetector,
) -> None:
    # перевес нулей: значение для 0 должно встречаться чаще
    chars = container_from_bits("100000000010000001")
    method = formatting_detector.detect(chars)
    assert method is not None
    assert method.zero_value == "28"
    assert method.one_value == "29"
