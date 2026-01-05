from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any, TypeVar

from chat_service.domain.common.errors.base import DomainError
from chat_service.domain.common.errors.time_errors import InconsistentTimeError

OIDType = TypeVar("OIDType")


@dataclass(eq=False, kw_only=True)
class BaseEntity[OIDType]:
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
    """

    id: OIDType

    created_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )

    updated_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
        kw_only=True,
    )

    def __post_init__(self) -> None:
        """Ensure timestamps are consistent."""
        if self.updated_at < self.created_at:
            msg = (
                f"{self.updated_at.strftime('%Y-%m-%d %H:%M:%S')}"
                f" cannot be earlier than"
                f" {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            raise InconsistentTimeError(
                msg,
            )

    def __setattr__(self, name: str, value: Any) -> None:  # noqa: ANN401
        """
        Prevents modifying the `id` after it's set.
        Other attributes can be changed as usual.
        """
        if name == "id" and getattr(self, "id", None) is not None:
            msg = "Changing entity ID is not permitted."
            raise DomainError(msg)
        super().__setattr__(name, value)

    def __eq__(self, other: object) -> bool:
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