from dataclasses import dataclass

from mathematical_algorithms_of_geometry_in_cryptography.domain.common.entities.base_entity import BaseEntity, OIDType


@dataclass(eq=False, kw_only=True)
class BaseAggregateRoot(BaseEntity[OIDType]): ...