from app.domain.entities.base import BaseEntity
from dataclasses import dataclass

from app.domain.values.mail import Email
from app.domain.values.user import UserName, UserSurname, UserURL


@dataclass(eq=False)
class UserEntity(BaseEntity):
    name: UserName
    surname: UserSurname
    email: Email
    url: UserURL
