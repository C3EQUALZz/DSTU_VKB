import math
from dataclasses import dataclass

from vulnfinder.domain.common.errors import DomainFieldError
from vulnfinder.domain.common.values.base import BaseValueObject


@dataclass(frozen=True, eq=True)
class SimilarityScore(BaseValueObject):
    value: float

    def _validate(self) -> None:
        if not 0.0 <= self.value <= 1.0:
            msg = "SimilarityScore must be between 0 and 1."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return f"{self.value:.3f}"


@dataclass(frozen=True, eq=True)
class QueryEmbedding(BaseValueObject):
    vector: tuple[float, ...]

    def _validate(self) -> None:
        if not self.vector:
            msg = "QueryEmbedding cannot be empty."
            raise DomainFieldError(msg)

        for value in self.vector:
            if not math.isfinite(value):
                msg = "QueryEmbedding contains non-finite values."
                raise DomainFieldError(msg)

    def __str__(self) -> str:
        return f"embedding[{len(self.vector)}]"

