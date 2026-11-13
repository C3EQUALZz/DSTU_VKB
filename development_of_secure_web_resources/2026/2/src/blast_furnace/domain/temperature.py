from dataclasses import dataclass
from math import isfinite


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
