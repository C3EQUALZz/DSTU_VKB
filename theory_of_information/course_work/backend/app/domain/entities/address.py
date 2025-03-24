from dataclasses import dataclass

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class AddressEntity(BaseEntity):
    country: str
    city: str
    street: str
    postal_code: str
