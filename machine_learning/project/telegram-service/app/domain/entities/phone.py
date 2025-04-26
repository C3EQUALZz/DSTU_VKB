from dataclasses import field
from datetime import datetime
from typing import Optional

from app.domain.entities.base import BaseEntity
from app.domain.values.phone import (
    PhoneNumber,
    VerificationStatus,
)


class PhoneNumberEntity(BaseEntity):
    number: PhoneNumber
    verification_status: VerificationStatus
    last_checked: Optional[datetime] = field(default=None)
