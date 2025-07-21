from dataclasses import dataclass, field
from typing import Generic, TypeVar, Hashable, Any

from cryptography_methods.domain.common.errors.base import DomainError
from cryptography_methods.domain.common.errors.time_errors import InconsistentTimeError
from cryptography_methods.domain.common.values import (
    CreateTime,
    UpdateTime,
)

OIDType = TypeVar("OIDType", bound=Hashable)


@dataclass(eq=False, kw_only=True)
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
        - Designed to be inherited by concrete entity classes
        - Supports any identifier type through generics
        - Forms the foundation of the domain model hierarchy
            ...
    """
    id: OIDType

    created_at: CreateTime = field(default_factory=lambda: CreateTime.now())
    updated_at: UpdateTime = field(default_factory=lambda: UpdateTime.now())

    def __post_init__(self) -> None:
        if self.updated_at.value < self.created_at.value:
            raise InconsistentTimeError(
                f"{self.updated_at.value.strftime('%Y-%m-%d %H:%M:%S')}"
                f" cannot be earlier than"
                f" {self.created_at.value.strftime('%Y-%m-%d %H:%M:%S')}",
            )

    def __setattr__(self, name: str, value: Any) -> None:
        """
        Prevents modifying the `id` after it's set.
        Other attributes can be changed as usual.
        """
        if name == "id_" and getattr(self, "id_", None) is not None:
            raise DomainError("Changing entity ID is not permitted.")
        super().__setattr__(name, value)

    def __eq__(self, other: object) -> bool:
        """
        Two entities are considered equal if they have the same `id`,
        regardless of other attribute values.
        """
        if other is None:
            return False

        if type(self) is not type(other):
            return False

        if isinstance(other, BaseEntity):
            return bool(other.id == self.id)

        return False

    def __hash__(self) -> int:
        """
        Generate a hash based on entity type and the immutable `id`.
        This allows entities to be used in hash-based collections and
        reduces the risk of hash collisions between different entity types.
        """
        return hash((type(self), self.id))
