"""Справочные значения с рисунка 2 методических указаний, страница 5.

Единицы измерения и направления изменений в источнике не заданы.
Эти значения не являются коэффициентами расчёта температуры.
"""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True, kw_only=True)
class BlastParameterEffect:
    parameter: str
    change: Decimal
    coke_consumption_change: Decimal
    productivity_change: Decimal


BLAST_PARAMETER_EFFECTS = (
    BlastParameterEffect(
        parameter="Температура дутья",
        change=Decimal("100"),
        coke_consumption_change=Decimal("0.5"),
        productivity_change=Decimal("1.0"),
    ),
    BlastParameterEffect(
        parameter="Горячая прочность кокса",
        change=Decimal("1"),
        coke_consumption_change=Decimal("1"),
        productivity_change=Decimal("1.6"),
    ),
    BlastParameterEffect(
        parameter="Расход природного газа",
        change=Decimal("10"),
        coke_consumption_change=Decimal("0.5"),
        productivity_change=Decimal("1.0"),
    ),
)
