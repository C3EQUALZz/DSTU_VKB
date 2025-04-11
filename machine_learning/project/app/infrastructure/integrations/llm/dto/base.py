from abc import ABC
from dataclasses import dataclass, asdict
from typing import Any


@dataclass(frozen=True)
class AbstractDTO(ABC):
    async def to_dict(self, exclude: set[str] | None = None, include: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data
