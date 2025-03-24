from dataclasses import dataclass

from app.domain.entities.base import BaseEntity
from app.domain.values.shared import URL
from app.domain.values.social_network import Platform


@dataclass(eq=False)
class SocialNetworkEntity(BaseEntity):
    platform: Platform
    url: URL
