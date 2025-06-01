import math

from app.application.analyzers.base import IAnalyzerComponent
from app.domain.calculators.base import IMetricsCalculator
from app.domain.calculators.dtos.halstead import HalsteadDTO
from typing import override, Final


class HalsteadMetricsCalculator(IMetricsCalculator[HalsteadDTO]):
    def __init__(self, analyzer: IAnalyzerComponent) -> None:
        self._analyzer: Final[IAnalyzerComponent] = analyzer

    @override
    def calculate(self) -> HalsteadDTO:

        metrics: dict[str, float | int] = {
            "η1": len(self._analyzer.operators),
            "η2": len(self._analyzer.operands),
            "N1": self._analyzer.stats.get("operators_count", 0),
            "N2": self._analyzer.stats.get("operands_count", 0),
            "η2*": len(self._analyzer.global_vars) + self._analyzer.stats.get("parameters", 0),
            "η": len(self._analyzer.operators) + len(self._analyzer.operands),
            "N": self._analyzer.stats.get("operators_count", 0) + self._analyzer.stats.get("operands_count", 0),
            "V": 0,
            "V*": 0,
            "L": 0,
            "λ": 0,
            "E": 0
        }

        try:
            metrics["V"] = metrics["N"] * math.log2(metrics["η"]) if metrics["η"] > 0 else 0
            combined = metrics["η2*"] + 2
            metrics["V*"] = combined * math.log2(combined) if combined > 0 else 0
            metrics["L"] = metrics["V*"] / metrics["V"] if metrics["V"] != 0 else 0
            metrics["λ"] = metrics["L"] * metrics["V*"]
            metrics["E"] = metrics["V"] / metrics["L"] if metrics["L"] != 0 else 0
        except (ValueError, ZeroDivisionError) as e:
            print(f"Ошибка при вычислении метрик: {e}")

        return HalsteadDTO(
            nu_1=metrics["η1"],
            nu_2=metrics["η2"],
            n_1=metrics["N1"],
            n_2=metrics["N2"],
            nu_2_with_starlet=metrics["η2*"],
            nu=metrics["η"],
            n=metrics["N"],
            v=metrics["V"],
            v_with_starlet=metrics["V*"],
            l=metrics["L"],
            lambda_=metrics["λ"],
            e=metrics["E"],
        )
