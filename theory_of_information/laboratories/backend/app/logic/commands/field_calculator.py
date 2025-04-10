from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class EvaluateExpressionInField(AbstractCommand):
    expression: str
    mod: int
