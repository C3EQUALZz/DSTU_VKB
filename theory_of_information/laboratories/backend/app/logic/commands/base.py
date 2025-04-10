from abc import ABC
from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional, Set


@dataclass(frozen=True)
class AbstractCommand(ABC):
    """
    Base command, from which any domain command should be inherited.
    Commands represents external operations, which must be executed.
    """

    async def to_dict(
        self,
        exclude: Optional[Set[str]] = None,
        include: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a dictionary representation of the model.

        exclude: set of model fields, which should be excluded from dictionary representation.
        include: set of model fields, which should be included into dictionary representation.
        """

        data: Dict[str, Any] = asdict(self)
        if exclude:
            for key in exclude:
                try:
                    del data[key]
                except KeyError:
                    pass

        if include:
            data.update(include)

        return data
