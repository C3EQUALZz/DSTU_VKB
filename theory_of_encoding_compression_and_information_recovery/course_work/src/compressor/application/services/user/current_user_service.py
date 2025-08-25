import logging
from typing import Final

from compressor.application.common.ports.access_revoker import AccessRevoker
from compressor.application.common.ports.identity_provider import IdentityProvider
from compressor.application.common.ports.user_query_gateway import UserQueryGateway
from compressor.application.services.user.constants import AUTHZ_NO_CURRENT_USER, AUTHZ_NOT_AUTHORIZED
from compressor.domain.users.entities.user import User
from compressor.domain.users.errors import AuthorizationError
from compressor.domain.users.values.user_id import UserID

logger: Final[logging.Logger] = logging.getLogger(__name__)


class CurrentUserService:
    def __init__(
            self,
            identity_provider: IdentityProvider,
            user_query_gateway: UserQueryGateway,
            access_revoker: AccessRevoker,
    ) -> None:
        self._identity_provider: Final[IdentityProvider] = identity_provider
        self._user_query_gateway: Final[UserQueryGateway] = user_query_gateway
        self._access_revoker: Final[AccessRevoker] = access_revoker

    async def get_current_user(self) -> User:
        current_user_id: UserID = await self._identity_provider.get_current_user_id()
        user: User | None = await self._user_query_gateway.read_by_id(current_user_id)

        if user is None or not user.is_active:
            logger.warning("%s ID: %s.", AUTHZ_NO_CURRENT_USER, current_user_id)
            await self._access_revoker.remove_all_user_access(current_user_id)
            raise AuthorizationError(AUTHZ_NOT_AUTHORIZED)

        return user
