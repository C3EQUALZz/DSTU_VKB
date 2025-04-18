from dataclasses import dataclass


@dataclass(frozen=True)
class EncodedAndPolynomDTO:
    terms: str
    encoded: str


@dataclass(frozen=True)
class EncodedAndMatrixDTO:
    encoded: str
    matrix: list[list[int]]
