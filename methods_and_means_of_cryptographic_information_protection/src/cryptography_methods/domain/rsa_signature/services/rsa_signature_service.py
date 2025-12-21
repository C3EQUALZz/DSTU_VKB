"""RSA-based digital signature service (separate from RSA encryption)."""

import hashlib
import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService,
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService,
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RSASignaturePublicKey:
    """Public key for RSA signature (e, n)."""

    e: int
    n: int


@dataclass(frozen=True, slots=True)
class RSASignaturePrivateKey:
    """Private key for RSA signature (d, n)."""

    d: int
    n: int


@dataclass(frozen=True, slots=True)
class RSASignatureKeyPair:
    """Key pair used for RSA signature scheme."""

    public_key: RSASignaturePublicKey
    private_key: RSASignaturePrivateKey
    p: int
    q: int


class RSASignatureService(DomainService):
    """Service for RSA key generation and PKCS#1 v1.5 signatures."""

    def __init__(
        self,
        prime_number_service: PrimeNumberService,
        modular_arithmetic_service: ModularArithmeticService,
    ) -> None:
        super().__init__()
        self._prime_service: Final[PrimeNumberService] = prime_number_service
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service
        logger.info("Initialized RSASignatureService")

    # ==========
    #  Key gen
    # ==========

    def generate_key_pair(
        self,
        key_size: int = 2048,
        min_prime_diff_bits: int = 64,
    ) -> RSASignatureKeyPair:
        """Generate RSA key pair for signature operations."""
        logger.info(
            "Starting RSA signature key generation with key_size=%s bits, min_prime_diff_bits=%s",
            key_size,
            min_prime_diff_bits,
        )
        prime_size = key_size // 2

        logger.info("[1] Generating prime numbers for signature keys...")
        p, q = self._generate_primes(prime_size, min_prime_diff_bits)
        logger.info("Generated p (%s bits): %s", p.bit_length(), p)
        logger.info("Generated q (%s bits): %s", q.bit_length(), q)

        logger.info("[2] Calculating n and phi(n)...")
        n = p * q
        phi = (p - 1) * (q - 1)
        logger.info("n (%s bits): %s", n.bit_length(), n)
        logger.info("phi(n) (%s bits): %s", phi.bit_length(), phi)

        logger.info("[3] Choosing private exponent d coprime with phi(n)...")
        d = self._generate_coprime(phi, key_size)
        logger.info("d (%s bits): %s", d.bit_length(), d)
        gcd, _, _ = self._modular_arithmetic.extended_euclidean(d, phi)
        logger.info("GCD(d, phi(n)) = %s", gcd)

        logger.info("[4] Computing public exponent e as modular inverse of d...")
        e = self._modular_arithmetic.mod_inverse(d, phi)
        if e is None:
            raise ValueError("Failed to find modular inverse for d mod phi(n)")
        logger.info("e (%s bits): %s", e.bit_length(), e)
        logger.info("Verification: (e*d) mod phi(n) = %s", (e * d) % phi)

        public_key = RSASignaturePublicKey(e=e, n=n)
        private_key = RSASignaturePrivateKey(d=d, n=n)

        logger.info("RSA signature key pair generated successfully")
        return RSASignatureKeyPair(
            public_key=public_key,
            private_key=private_key,
            p=p,
            q=q,
        )

    def _generate_primes(
        self,
        prime_size: int,
        min_prime_diff_bits: int,
    ) -> tuple[int, int]:
        """Generate two distinct prime numbers for RSA signature."""
        logger.debug(
            "Generating two distinct primes for signature keys of size %s bits with min_diff=%s bits",
            prime_size,
            min_prime_diff_bits,
        )
        max_attempts = 100
        attempt = 0

        while attempt < max_attempts:
            p = self._prime_service.generate_large_prime(prime_size)
            q = self._prime_service.generate_large_prime(prime_size)

            diff = abs(p - q)
            min_diff = 1 << min_prime_diff_bits

            if diff >= min_diff:
                logger.debug(
                    "Generated primes for signature with difference %s bits (>= %s)",
                    diff.bit_length(),
                    min_prime_diff_bits,
                )
                return p, q

            attempt += 1
            logger.debug(
                "Attempt %s: Signature primes too close (diff=%s bits), retrying...",
                attempt,
                diff.bit_length(),
            )

        raise RuntimeError(
            f"Failed to generate sufficiently different primes for signature after {max_attempts} attempts"
        )

    def _generate_coprime(self, m: int, key_size: int) -> int:
        """Generate a number d coprime to m."""
        logger.debug("Generating coprime d to m (bits=%s) for signature keys", m.bit_length())
        max_attempts = 1000
        attempt = 0

        while attempt < max_attempts:
            d = self._generate_random_big_integer(key_size) % m
            if d <= 1:
                attempt += 1
                continue

            gcd, _, _ = self._modular_arithmetic.extended_euclidean(d, m)
            if gcd == 1:
                logger.debug("Found coprime d after %s attempts", attempt + 1)
                return d

            attempt += 1

        raise RuntimeError(
            f"Failed to generate coprime d for signature after {max_attempts} attempts"
        )

    @staticmethod
    def _generate_random_big_integer(bit_length: int) -> int:
        """Generate random big integer of specified bit length."""
        import secrets

        num_bytes = (bit_length + 7) // 8
        random_bytes = secrets.token_bytes(num_bytes)
        candidate = int.from_bytes(random_bytes, byteorder="big", signed=False)

        if bit_length % 8 != 0:
            mask = (1 << (bit_length % 8)) - 1
            candidate &= mask

        max_value = 1 << bit_length
        if candidate >= max_value:
            candidate %= max_value

        return candidate

    # ==========
    #  Hashing
    # ==========

    @staticmethod
    def compute_hash(data: bytes) -> bytes:
        """Compute SHA-256 hash of data."""
        logger.info("Computing SHA-256 hash for %s bytes", len(data))
        digest = hashlib.sha256(data).digest()
        logger.debug("SHA-256 hash: %s", digest.hex())
        return digest

    # ==========
    #  Sign/Verify (PKCS#1 v1.5 + SHA-256)
    # ==========

    def sign_hash(
        self,
        hash_bytes: bytes,
        private_key: RSASignaturePrivateKey,
    ) -> bytes:
        """Create RSA PKCS#1 v1.5 signature for given SHA-256 hash."""
        n = private_key.n
        d = private_key.d
        k = (n.bit_length() + 7) // 8

        if len(hash_bytes) != 32:
            raise ValueError("Expected SHA-256 hash (32 bytes)")

        logger.info("Creating RSA signature (k=%s bytes)", k)

        em = self._encode_pkcs1_v1_5_sha256(hash_bytes, k)
        m_int = int.from_bytes(em, "big")
        s_int = self._modular_arithmetic.mod_pow(m_int, d, n)
        signature = s_int.to_bytes(k, "big")

        logger.debug("RSA signature (hex): %s", signature.hex())
        return signature

    def verify_signature(
        self,
        hash_bytes: bytes,
        signature: bytes,
        public_key: RSASignaturePublicKey,
    ) -> bool:
        """Verify RSA PKCS#1 v1.5 signature for given SHA-256 hash."""
        if len(hash_bytes) != 32:
            raise ValueError("Expected SHA-256 hash (32 bytes)")

        n = public_key.n
        e = public_key.e
        k = (n.bit_length() + 7) // 8

        logger.info("Verifying RSA signature (k=%s bytes)", k)

        if len(signature) != k:
            # Allow shorter signatures by left-padding.
            logger.debug(
                "Signature length (%s) != modulus length (%s), left-padding if shorter", len(signature), k
            )
            if len(signature) > k:
                return False
            signature = signature.rjust(k, b"\x00")

        s_int = int.from_bytes(signature, "big")
        m_int = self._modular_arithmetic.mod_pow(s_int, e, n)
        em = m_int.to_bytes(k, "big")

        if not self._verify_pkcs1_v1_5_sha256_encoding(hash_bytes, em):
            logger.info("RSA signature verification failed: encoding mismatch")
            return False

        logger.info("RSA signature verification succeeded")
        return True

    @staticmethod
    def _encode_pkcs1_v1_5_sha256(hash_bytes: bytes, k: int) -> bytes:
        """Encode SHA-256 hash using PKCS#1 v1.5 for signatures."""
        # ASN.1 DER DigestInfo for SHA-256:
        #  SEQUENCE {
        #    SEQUENCE { OID sha256, NULL }
        #    OCTET STRING (32 bytes hash)
        #  }
        digest_info_prefix = bytes.fromhex(
            "3031300d060960864801650304020105000420"
        )  # 19 bytes

        t = digest_info_prefix + hash_bytes
        if len(t) + 11 > k:
            raise ValueError("Intended encoded message length too short for PKCS#1 v1.5")

        ps_len = k - len(t) - 3
        ps = b"\xff" * ps_len
        em = b"\x00\x01" + ps + b"\x00" + t
        return em

    @staticmethod
    def _verify_pkcs1_v1_5_sha256_encoding(hash_bytes: bytes, em: bytes) -> bool:
        """Verify PKCS#1 v1.5 encoding for SHA-256."""
        k = len(em)
        if k < 11:
            return False
        if not (em[0] == 0x00 and em[1] == 0x01):
            return False

        # Skip PS
        i = 2
        while i < k and em[i] == 0xFF:
            i += 1
        if i >= k or em[i] != 0x00:
            return False
        i += 1

        digest_info_prefix = bytes.fromhex(
            "3031300d060960864801650304020105000420"
        )
        if i + len(digest_info_prefix) + 32 != k:
            return False

        if em[i : i + len(digest_info_prefix)] != digest_info_prefix:
            return False

        h_prime = em[-32:]
        return h_prime == hash_bytes

    # ==================
    #  Key I/O helpers
    # ==================

    @staticmethod
    def save_public_key(public_key: RSASignaturePublicKey, file_path: Path) -> None:
        """Save RSA signature public key to file (e, n per line)."""
        logger.info("Saving RSA signature public key to file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"{public_key.e}\n")
            f.write(f"{public_key.n}\n")

    @staticmethod
    def save_private_key(private_key: RSASignaturePrivateKey, file_path: Path) -> None:
        """Save RSA signature private key to file (d, n per line)."""
        logger.info("Saving RSA signature private key to file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"{private_key.d}\n")
            f.write(f"{private_key.n}\n")

    @staticmethod
    def load_public_key(file_path: Path) -> RSASignaturePublicKey:
        """Load RSA signature public key from file."""
        logger.info("Loading RSA signature public key from file: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Public key file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 2:
            raise ValueError("Invalid RSA signature public key file: expected 2 lines (e, n)")

        e = int(lines[0])
        n = int(lines[1])
        return RSASignaturePublicKey(e=e, n=n)

    @staticmethod
    def load_private_key(file_path: Path) -> RSASignaturePrivateKey:
        """Load RSA signature private key from file."""
        logger.info("Loading RSA signature private key from file: %s", file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"Private key file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f.readlines()]

        if len(lines) < 2:
            raise ValueError("Invalid RSA signature private key file: expected 2 lines (d, n)")

        d = int(lines[0])
        n = int(lines[1])
        return RSASignaturePrivateKey(d=d, n=n)



