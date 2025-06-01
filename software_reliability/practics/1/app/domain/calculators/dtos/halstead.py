from dataclasses import dataclass
from app.domain.calculators.dtos.base import BaseDTO


@dataclass(frozen=True)
class HalsteadDTO(BaseDTO):
    nu_1: int
    nu_2: int
    n_1: int
    n_2: int
    nu_2_with_starlet: int
    nu: int
    n: int
    v: float
    v_with_starlet: float
    l: float
    lambda_: float
    e: float
