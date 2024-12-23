from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class User(BaseEntity):
    name: str
    email: str
    password: str
    is_active: bool
    is_superuser: bool
    verified_at: datetime
    updated_at: datetime
    created_at: datetime

