from dataclasses import dataclass, field
from typing import Generic, TypeVar

from cryptography_methods.domain.common.errors.time_errors import InconsistentTimeError
from cryptography_methods.domain.common.values import (
    CreateTime,
    DeleteTime,
    UpdateTime,
)

OIDType = TypeVar("OIDType")


@dataclass
class BaseEntity(Generic[OIDType]):
    """Abstract base class for all domain entities.

    What is domain entity:
    - https://wempe.dev/blog/domain-driven-design-entities-value-objects
    - https://medium.com/@michaelmaurice410/what-is-an-entity-unveiling-the-core-of-domain-driven-design-and-clean-architecture-84b492c4398d
    - https://habr.com/ru/articles/787460/
    - https://ru.wikipedia.org/wiki/%D0%9F%D1%80%D0%B5%D0%B4%D0%BC%D0%B5%D1%82%D0%BD%D0%BE-%D0%BE%D1%80%D0%B8%D0%B5%D0%BD%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%BD%D0%BE%D0%B5_%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D0%B5#%D0%A1%D1%83%D1%89%D0%BD%D0%BE%D1%81%D1%82%D1%8C

    Provides the fundamental structure for domain entities with generic
    identifier support. All concrete domain entities should inherit from
    this class.

    Attributes:
        id: The unique identifier of the entity. Type is parameterized
            to support different identifier types (int, UUID, etc.) for
            different entities.

    Type Variables:
        OIDType: The type parameter for the entity's identifier.

    Note:
        - Uses @dataclass for automatic boilerplate reduction
        - Designed to be inherited by concrete entity classes
        - Supports any identifier type through generics
        - Forms the foundation of the domain model hierarchy
            ...
    """

    id: OIDType

    created_at: CreateTime = field(
        default_factory=lambda: CreateTime.now(),
        kw_only=True,
    )

    updated_at: UpdateTime = field(
        default_factory=lambda: UpdateTime.now(),
        kw_only=True,
    )

    deleted_at: DeleteTime = field(
        default_factory=lambda: DeleteTime.create_not_deleted(),
        kw_only=True,
    )

    def __post_init__(self) -> None:
        """Ensure timestamps are consistent."""
        if self.updated_at.value < self.created_at.value:
            raise InconsistentTimeError(
                f"{self.updated_at.value.strftime('%Y-%m-%d %H:%M:%S')}"
                f" cannot be earlier than"
                f" {self.created_at.value.strftime('%Y-%m-%d %H:%M:%S')}",
            )

    def __eq__(self, other: object) -> bool:
        if other is None:
            return False

        if type(self) is not type(other):
            return False

        if isinstance(other, BaseEntity):
            return bool(other.id == self.id)

        return False
