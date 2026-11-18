from typing import Protocol

from blast_furnace.domain.temperature import BlastParameters


class CalculationLog(Protocol):
    def append(
        self, parameters: BlastParameters, result: float, comment: str
    ) -> None: ...


class CalculateTemperature:
    def __init__(self, log: CalculationLog) -> None:
        self._log = log

    def execute(self, parameters: BlastParameters, comment: str) -> float:
        result = parameters.theoretical_temperature()
        self._log.append(parameters, result, comment)
        return result
