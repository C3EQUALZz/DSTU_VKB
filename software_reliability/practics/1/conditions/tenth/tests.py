import pytest

from conditions.tenth.main import compress


@pytest.mark.parametrize(
    "input_str, expected",
    [
        ("hello world", "helloworld"),
        ("   leading", "leading"),
        ("trailing   ", "trailing"),
        ("   ", ""),
        ("no spaces", "no spaces"),
        ("  a  b  c  ", "abc"),
        ("", ""),
        ("   multiple     spaces", "multiplespaces"),
    ],
)
def test_compress(input_str: str, expected: str) -> None:
    assert compress(input_str) == expected
