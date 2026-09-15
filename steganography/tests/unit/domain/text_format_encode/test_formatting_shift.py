"""The relative carrier values shared by the writer and detector."""

import pytest

from steganography.domain.common.services.formatting_shift import shifted_value
from steganography.domain.common.value_objects.formatting_param import FormattingParam


@pytest.mark.parametrize(("param", "value", "expected"), [
    (FormattingParam.SIZE, "28", "29"),
    (FormattingParam.SCALE, "100", "99"),
    (FormattingParam.SPACING, "-2", "-1"),
    (FormattingParam.COLOR, "000000", "000001"),
    (FormattingParam.COLOR, "abcdef", "ABCDF0"),
    (FormattingParam.COLOR, "FFFFFF", None),
    (FormattingParam.COLOR, "auto", None),
    (FormattingParam.COLOR, "GGGGGG", None),
    (FormattingParam.SIZE, "invalid", None),
    (FormattingParam.SIZE, "0", None),
    (FormattingParam.SCALE, "1", None),
    (FormattingParam.HIGHLIGHT, "yellow", None),
])
def test_shifted_value(param: FormattingParam, value: str, expected: str | None) -> None:
    assert shifted_value(param, value) == expected
