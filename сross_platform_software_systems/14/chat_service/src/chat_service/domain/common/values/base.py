from abc import ABC, abstractmethod
from dataclasses import dataclass, fields

from chat_service.domain.common.errors.base import DomainFieldError


@dataclass(frozen=True, eq=True, unsafe_hash=True)
class BaseValueObject(ABC):
    """
    Base class for immutable value objects (VO) in the domain.
    - Defined by its attributes, which must also be immutable.

    For simple cases where immutability and additional behavior aren't required,
    consider using `NewType` from `typing` as a lightweight alternative
    to inheriting from this class.
    """

    def __post_init__(self) -> None:
        if not fields(self):
            msg = f"{type(self).__name__} must have at least one field!"
            raise DomainFieldError(
                msg,
            )

        self._validate()

    @abstractmethod
    def _validate(self) -> None:
        """
        Check that a value is valid to create this value object.
        """
        raise NotImplementedError

    @abstractmethod
    def __str__(self) -> str:
        """
        :return: returns a string representation of this value object.
        """
        raise NotImplementedError
