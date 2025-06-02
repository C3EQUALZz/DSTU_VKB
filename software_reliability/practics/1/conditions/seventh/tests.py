from typing import Tuple

import pytest

from conditions.seventh.main import minmax


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (5, 3, (5, 3)),
        (3, 5, (5, 3)),
        (0, 0, (0, 0)),
        (-1, -5, (-1, -5)),
        (2.5, 2.0, (2.5, 2.0)),
    ]
)
def test_minmax(x: int, y: int, expected: Tuple[int, int]) -> None:
    assert minmax(x, y) == expected
