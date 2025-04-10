import contextlib
from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any


@dataclass(frozen=True)
class AbstractCommand(ABC):
    """
    Base command, from which any domain command should be inherited.
    Commands represents external operations, which must be executed.
    """

    async def to_dict(self, exclude: set[str] | None = None, include: dict[str, Any] | None = None) -> dict[str, Any]:
        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                with contextlib.suppress(KeyError):
                    del data[key]

        if include:
            data.update(include)

        return data
