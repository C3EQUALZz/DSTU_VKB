from chat_service.domain.common.errors.base import DomainFieldError
from chat_service.domain.common.values.base import BaseValueObject


class AccessToken(BaseValueObject):
    """Value object representing an access token for a chat.
    
    This token allows external access to the chat without authentication.
    """

    value: str

    def _validate(self) -> None:
        """Validate the access token."""
        if not self.value:
            msg = "Access token cannot be empty."
            raise DomainFieldError(msg)
        if len(self.value) < 8:
            msg = "Access token must be at least 8 characters long."
            raise DomainFieldError(msg)

    def __str__(self) -> str:
        return self.value

