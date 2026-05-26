"""Тесты дефолтных значений сокрытия."""

import pytest

from steganography.domain.common.value_objects.formatting_param import (
    FormattingParam,
)
from steganography.domain.text_format_encode.services.hiding_value_defaults import (
    HidingValueDefaults,
)


@pytest.fixture
def defaults() -> HidingValueDefaults:
    return HidingValueDefaults()


@pytest.mark.parametrize("param", list(FormattingParam))
def test_every_param_has_distinct_pair(
    defaults: HidingValueDefaults, param: FormattingParam,
) -> None:
    zero, one = defaults.for_param(param)
    assert zero != one
