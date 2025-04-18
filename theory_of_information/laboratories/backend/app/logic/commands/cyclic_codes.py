from dataclasses import dataclass

from app.logic.commands.base import AbstractCommand


@dataclass(frozen=True)
class EncodeCyclicCodeWithMatrixCommand(AbstractCommand):
    data: str
    matrix: list[list[int]]


@dataclass(frozen=True)
class EncodeCyclicCodeWithPolynomCommand(AbstractCommand):
    data: str
    polynom: str
    n: int


@dataclass(frozen=True)
class DecodeCyclicCodeWithPolynomCommand(AbstractCommand):
    data: str
    polynom: str
    n: int



