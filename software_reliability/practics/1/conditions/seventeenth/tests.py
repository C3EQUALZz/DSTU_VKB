import pytest

from conditions.seventeenth.main import cube_root


@pytest.mark.parametrize(
    "x, expected",
    [
        (1.0, 1.0),
        (0.5, 0.7937005259840998),
        (-0.5, -0.7937005259840998),
        (0.000001, 0.001),
        (0.25, 0.6299605249474369),
        (-0.25, -0.6299605249474369),
    ],
)
def test_cube_root(x: float, expected: float) -> None:
    result = cube_root(x)
    assert abs(result - expected) < 1


@pytest.mark.parametrize(
    "x",
    [
        2.0,
        -2.0,
        0.0
    ]
)
def test_invalid_x(x: float) -> None:
    with pytest.raises(ValueError):
        cube_root(x)
