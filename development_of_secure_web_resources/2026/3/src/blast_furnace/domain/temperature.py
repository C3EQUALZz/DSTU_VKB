from dataclasses import dataclass
from math import isfinite

from blast_furnace.domain.services.calculations import calculate_ttg


@dataclass(frozen=True, slots=True)
class BlastParameters:
    t_blast: float
    humidity: float
    oxygen: float
    gas: float

    def __post_init__(self) -> None:
        for label, value, lower, upper in (
            ("Температура дутья", self.t_blast, 900, 1300),
            ("Влажность дутья", self.humidity, 1, 40),
            ("Содержание кислорода", self.oxygen, 21, 35),
            ("Расход природного газа", self.gas, 0, 15),
        ):
            if not isfinite(value) or not lower <= value <= upper:
                raise ValueError(f"{label}: введите число от {lower} до {upper}.")

    def theoretical_temperature(self) -> float:
        return calculate_ttg(self.t_blast, self.humidity, self.oxygen, self.gas)
