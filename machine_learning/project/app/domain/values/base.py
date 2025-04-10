from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Generic, TypeVar

T = TypeVar("T", bound=Any)


@dataclass
class BaseValueObject(ABC, Generic[T]):
    """
    Base value object, from which any domain value object should be inherited.
    """

    value: T

    def __post_init__(self) -> None:
        self.validate()

    @abstractmethod
    def validate(self) -> None:
        """
        Method that validates that the value object (field of domain model) is valid.
        :return: raises exception if validation fails in other case returns nothing.
        """
        ...

    @abstractmethod
    def as_generic_type(self) -> T:
        """
        returns generic type of the value object for saving in database and etc.
        :return: a specific base type from Python
        """
        ...