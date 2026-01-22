from uuid import UUID, uuid4

from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider


class Uuid4Provider(UUIDProvider):
    def __call__(self) -> UUID:
        return uuid4()

