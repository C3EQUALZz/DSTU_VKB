from typing import Protocol

from blast_furnace.domain.services.calculations import calculate_ttg
from blast_furnace.domain.temperature import BlastParameters


class CalculationLog(Protocol):
    def append(
        self, parameters: BlastParameters, result: float, comment: str
    ) -> None: ...


class CalculateTemperature:
    def __init__(self, log: CalculationLog) -> None:
        self._log = log

    def execute(self, parameters: BlastParameters, comment: str) -> float:
        result = calculate_ttg(
            parameters.t_blast, parameters.humidity, parameters.oxygen, parameters.gas
        )
        self._log.append(parameters, result, comment)
        return result
