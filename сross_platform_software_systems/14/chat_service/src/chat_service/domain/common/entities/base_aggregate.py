from dataclasses import dataclass

from chat_service.domain.common.entities.base_entity import BaseEntity, OIDType


@dataclass(eq=False, kw_only=True)
class BaseAggregateRoot(BaseEntity[OIDType]): ...