"""Value objects for RSA keys."""
import logging
from dataclasses import dataclass
from typing import Final

from cryptography_methods.domain.common.values.base import BaseValueObject

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSAPublicKey(BaseValueObject):
    """Value object representing RSA public key (e, n)."""

    e: int
    n: int

    def _validate(self) -> None:
        """Validate public key values."""
        if self.e <= 1:
            raise ValueError("Public exponent e must be greater than 1")
        if self.n <= 1:
            raise ValueError("Modulus n must be greater than 1")
        logger.debug("Created RSA public key with e=%s, n=%s", self.e, self.n)

    def __str__(self) -> str:
        """String representation of public key."""
        return f"RSAPublicKey(e={self.e}, n={self.n})"


@dataclass(frozen=True, slots=True)
class RSAPrivateKey(BaseValueObject):
    """Value object representing RSA private key (d, n)."""

    d: int
    n: int

    def _validate(self) -> None:
        """Validate private key values."""
        if self.d <= 1:
            raise ValueError("Private exponent d must be greater than 1")
        if self.n <= 1:
            raise ValueError("Modulus n must be greater than 1")
        logger.debug("Created RSA private key with d=%s, n=%s", self.d, self.n)

    def __str__(self) -> str:
        """String representation of private key."""
        return f"RSAPrivateKey(d={self.d}, n={self.n})"

