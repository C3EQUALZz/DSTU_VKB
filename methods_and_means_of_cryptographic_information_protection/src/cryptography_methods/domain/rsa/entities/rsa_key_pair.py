"""RSA key pair entity."""
import logging
from dataclasses import dataclass
from typing import Final
from uuid import UUID

from cryptography_methods.domain.common.entities.base_entity import BaseEntity
from cryptography_methods.domain.rsa.values.rsa_key import RSAPrivateKey, RSAPublicKey

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(eq=False, kw_only=True)
class RSAKeyPair(BaseEntity[UUID]):
    """Entity representing RSA key pair."""

    public_key: RSAPublicKey
    private_key: RSAPrivateKey
    p: int
    q: int

    def __post_init__(self) -> None:
        """Validate key pair."""
        super().__post_init__()
        if self.p <= 1 or self.q <= 1:
            raise ValueError("Primes p and q must be greater than 1")
        if self.public_key.n != self.private_key.n:
            raise ValueError("Modulus n must be the same in both keys")
        logger.debug(
            "Created RSA key pair with id=%s, n=%s bits",
            self.id,
            self.public_key.n.bit_length()
        )

