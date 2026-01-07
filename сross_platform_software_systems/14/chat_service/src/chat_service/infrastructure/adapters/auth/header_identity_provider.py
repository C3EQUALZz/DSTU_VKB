"""Identity provider that extracts user ID from X-User-ID header.

This adapter is designed to work with API Gateway pattern where:
- API Gateway (e.g., Nginx) validates JWT token
- Gateway extracts user ID from token and adds it to X-User-ID header
- This adapter reads the header and provides user ID to the application layer
"""
import logging
from typing import Final
from uuid import UUID

from starlette.requests import Request

from chat_service.application.common.ports.identity_provider import IdentityProvider
from chat_service.domain.user.errors import AuthorizationError
from chat_service.domain.user.values.user_id import UserID

log: Final[logging.Logger] = logging.getLogger(__name__)

# Header name that API Gateway uses to pass user ID
X_USER_ID_HEADER: Final[str] = "X-User-ID"

# Log messages
USER_ID_NOT_FOUND_IN_HEADER: Final[str] = "User ID not found in X-User-ID header"
INVALID_USER_ID_FORMAT: Final[str] = "Invalid user ID format in X-User-ID header"


class HeaderIdentityProvider(IdentityProvider):
    """Identity provider that extracts user ID from X-User-ID header.

    This implementation expects that API Gateway (e.g., Nginx) has already
    validated the JWT token and extracted the user ID, placing it in the
    X-User-ID header.
    """

    def __init__(self, request: Request) -> None:
        """Initialize the identity provider with a request object.

        Args:
            request: Starlette request object containing headers
        """
        self._request: Final[Request] = request

    async def get_current_user_id(self) -> UserID:
        """Extract user ID from X-User-ID header.

        Returns:
            UserID: The user ID extracted from the header

        Raises:
            AuthorizationError: If the header is missing or contains invalid format
        """
        user_id_str: str | None = self._request.headers.get(X_USER_ID_HEADER)

        if user_id_str is None:
            log.debug("%s", USER_ID_NOT_FOUND_IN_HEADER)
            msg = "User ID not found in request headers"
            raise AuthorizationError(msg)

        try:
            user_id_uuid: UUID = UUID(user_id_str)
        except ValueError as e:
            log.warning(
                "%s: %s. Header value: %s",
                INVALID_USER_ID_FORMAT,
                e,
                user_id_str,
            )
            msg = f"Invalid user ID format: {user_id_str}"
            raise AuthorizationError(msg) from e

        return UserID(user_id_uuid)

