import pytest

from blast_furnace.domain.services.calculations import calculate_ttg
from blast_furnace.domain.temperature import BlastParameters


@pytest.mark.parametrize(
    ("parameters", "expected"),
    [
        ((1000, 10, 21, 0), 2201.0),
        ((1200, 15, 25, 8), 2080.0),
        ((1100, 20, 23, 5), 2048.0),
        ((1300, 1, 35, 0), 3076.6),
    ],
)
def test_assignment_control_values(
    parameters: tuple[float, float, float, float], expected: float
) -> None:
    assert calculate_ttg(*parameters) == pytest.approx(expected)


@pytest.mark.parametrize(
    ("parameters", "delta"),
    [
        ((1100, 10, 21, 0), 75),
        ((1000, 11, 21, 0), -5.4),
        ((1000, 10, 22, 0), 43),
        ((1000, 10, 21, 1), -52),
    ],
)
def test_physical_direction_of_coefficients(
    parameters: tuple[float, float, float, float], delta: float
) -> None:
    assert calculate_ttg(*parameters) - 2201 == pytest.approx(delta)


@pytest.mark.parametrize("temperature", [899, 1301, float("nan"), float("inf")])
def test_invalid_domain_parameters(temperature: float) -> None:
    with pytest.raises(ValueError, match="Температура дутья"):
        BlastParameters(temperature, 10, 21, 0)
