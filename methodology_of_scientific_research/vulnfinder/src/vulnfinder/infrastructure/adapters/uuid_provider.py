from uuid import UUID, uuid4

from typing_extensions import override

from vulnfinder.domain.common.ports.uuid_provider import UUIDProvider


class Uuid4Provider(UUIDProvider):
    @override
    def __call__(self) -> UUID:
        return uuid4()
