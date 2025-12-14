"""RSA cryptography service."""
import logging
import secrets
from pathlib import Path
from typing import Final

from cryptography_methods.domain.common.services.base import DomainService
from cryptography_methods.domain.rsa.entities.rsa_key_pair import RSAKeyPair
from cryptography_methods.domain.rsa.values.rsa_key import RSAPrivateKey, RSAPublicKey
from cryptography_methods.domain.zero_knowledge_proof.services.modular_arithmetic_service import (
    ModularArithmeticService
)
from cryptography_methods.domain.zero_knowledge_proof.services.prime_number_service import (
    PrimeNumberService
)

logger: Final[logging.Logger] = logging.getLogger(__name__)


class RSAService(DomainService):
    """Service for RSA key generation, encryption and decryption."""

    def __init__(
        self,
        prime_number_service: PrimeNumberService,
        modular_arithmetic_service: ModularArithmeticService,
    ) -> None:
        """Initialize RSA service.

        Args:
            prime_number_service: Service for prime number generation
            modular_arithmetic_service: Service for modular arithmetic operations
        """
        super().__init__()
        self._prime_service: Final[PrimeNumberService] = prime_number_service
        self._modular_arithmetic: Final[ModularArithmeticService] = modular_arithmetic_service

        logger.info("Initialized RSA service")

    def generate_key_pair(
        self,
        key_size: int = 2048,
        min_prime_diff_bits: int = 64,
    ) -> RSAKeyPair:
        """Generate RSA key pair.

        Args:
            key_size: Size of RSA key in bits (default: 2048)
            min_prime_diff_bits: Minimum difference between primes in bits (default: 64)

        Returns:
            RSA key pair with public and private keys
        """
        logger.info(
            "Starting RSA key pair generation with key_size=%s bits, min_prime_diff_bits=%s",
            key_size,
            min_prime_diff_bits
        )
        prime_size = key_size // 2

        # Generate primes
        logger.info("[1] Generating prime numbers...")
        p, q = self._generate_primes(prime_size, min_prime_diff_bits)
        logger.info("Generated p (%s bits): %s", p.bit_length(), p)
        logger.info("Generated q (%s bits): %s", q.bit_length(), q)

        # Calculate n and m (Euler's totient function)
        logger.info("[2] Calculating n and m...")
        n = p * q
        m = (p - 1) * (q - 1)
        logger.info("n (%s bits): %s", n.bit_length(), n)
        logger.info("m (%s bits): %s", m.bit_length(), m)

        # Generate d (private exponent)
        logger.info("[3] Generating private exponent d...")
        d = self._generate_coprime(m, key_size)
        logger.info("d (%s bits): %s", d.bit_length(), d)
        gcd = self._modular_arithmetic.extended_euclidean(d, m)[0]
        logger.info("GCD(d, m): %s", gcd)

        # Find e (public exponent) - modular inverse of d
        logger.info("[4] Finding public exponent e...")
        e = self._modular_arithmetic.mod_inverse(d, m)
        if e is None:
            raise ValueError("Failed to find modular inverse for d mod m")
        logger.info("e (%s bits): %s", e.bit_length(), e)
        verification = (e * d) % m
        logger.info("Verification: (e*d) mod m = %s", verification)

        public_key = RSAPublicKey(e=e, n=n)
        private_key = RSAPrivateKey(d=d, n=n)

        # Generate UUID for key pair
        from uuid import uuid4
        key_pair = RSAKeyPair(
            id=uuid4(),
            public_key=public_key,
            private_key=private_key,
            p=p,
            q=q
        )

        logger.info("Successfully generated RSA key pair with id=%s", key_pair.id)
        return key_pair

    def encrypt(self, message: str, public_key: RSAPublicKey) -> list[int]:
        """Encrypt message using RSA public key.

        Args:
            message: Message to encrypt
            public_key: RSA public key

        Returns:
            List of encrypted integers
        """
        logger.info("Starting RSA encryption for message of length %s", len(message))
        encrypted: list[int] = []

        for i, char in enumerate(message):
            char_code = ord(char)
            encrypted_char = self._modular_arithmetic.mod_pow(char_code, public_key.e, public_key.n)
            encrypted.append(encrypted_char)
            logger.debug("Encrypted character %s (%s) -> %s", i, char, encrypted_char)

        logger.info("Successfully encrypted message, result length: %s", len(encrypted))
        return encrypted

    def decrypt(self, encrypted: list[int], private_key: RSAPrivateKey) -> str:
        """Decrypt message using RSA private key.

        Args:
            encrypted: List of encrypted integers
            private_key: RSA private key

        Returns:
            Decrypted message string
        """
        logger.info("Starting RSA decryption for %s encrypted blocks", len(encrypted))
        decrypted_chars: list[str] = []

        for i, encrypted_char in enumerate(encrypted):
            decrypted_code = self._modular_arithmetic.mod_pow(
                encrypted_char, private_key.d, private_key.n
            )
            decrypted_char = chr(decrypted_code)
            decrypted_chars.append(decrypted_char)
            logger.debug("Decrypted block %s (%s) -> %s", i, encrypted_char, decrypted_char)

        result = "".join(decrypted_chars)
        logger.info("Successfully decrypted message, result length: %s", len(result))
        return result

    def _generate_primes(
        self,
        prime_size: int,
        min_prime_diff_bits: int,
    ) -> tuple[int, int]:
        """Generate two distinct prime numbers.

        Args:
            prime_size: Size of each prime number in bits
            min_prime_diff_bits: Minimum difference between primes in bits

        Returns:
            Tuple of (p, q) prime numbers
        """
        logger.debug(
            "Generating two distinct primes of size %s bits with min_diff=%s bits",
            prime_size,
            min_prime_diff_bits
        )
        max_attempts = 100
        attempt = 0

        while attempt < max_attempts:
            p = self._prime_service.generate_large_prime(prime_size)
            q = self._prime_service.generate_large_prime(prime_size)

            # Ensure primes are sufficiently different
            diff = abs(p - q)
            min_diff = 1 << min_prime_diff_bits

            if diff >= min_diff:
                logger.debug(
                    "Generated primes with difference %s bits (>= %s)",
                    diff.bit_length(),
                    min_prime_diff_bits
                )
                return p, q

            attempt += 1
            logger.debug(
                "Attempt %s: Primes too close (diff=%s bits), retrying...",
                attempt,
                diff.bit_length()
            )

        raise RuntimeError(
            f"Failed to generate sufficiently different primes after {max_attempts} attempts"
        )

    def _generate_coprime(self, m: int, key_size: int) -> int:
        """Generate a number coprime to m.

        Args:
            m: Number to find coprime for
            key_size: Size of key in bits for generating random number

        Returns:
            Number coprime to m
        """
        logger.debug("Generating number coprime to m (%s bits) with key_size=%s", m.bit_length(), key_size)
        max_attempts = 1000
        attempt = 0

        while attempt < max_attempts:
            # Generate random number of key_size bits, then take modulo m
            # (as in C# code: d = RandomBigInteger(KEY_SIZE, rand); d = d % m)
            d = self._generate_random_big_integer(key_size)
            d = d % m

            # Ensure d > 1 (as in C# code: while (d <= 1 || ...))
            if d <= 1:
                attempt += 1
                continue

            # Check if coprime
            gcd, _, _ = self._modular_arithmetic.extended_euclidean(d, m)
            if gcd == 1:
                logger.debug("Found coprime d after %s attempts", attempt + 1)
                return d

            attempt += 1

        raise RuntimeError(
            f"Failed to generate coprime number after {max_attempts} attempts"
        )

    @staticmethod
    def _generate_random_big_integer(bit_length: int) -> int:
        """Generate random big integer of specified bit length.

        Args:
            bit_length: Bit length of the number

        Returns:
            Random integer of specified bit length
        """
        num_bytes = (bit_length + 7) // 8
        random_bytes = secrets.token_bytes(num_bytes)
        candidate = int.from_bytes(random_bytes, byteorder='big', signed=False)
        
        # Mask to ensure correct bit length (as in C# code)
        if bit_length % 8 != 0:
            mask = (1 << (bit_length % 8)) - 1
            candidate = candidate & mask
        
        # Ensure the number has the correct bit length
        max_value = 1 << bit_length
        if candidate >= max_value:
            candidate = candidate % max_value
        
        return candidate

    @staticmethod
    def _generate_random_big_integer_in_range(min_value: int, max_value: int) -> int:
        """Generate random integer in range [min_value, max_value).

        Args:
            min_value: Minimum value (inclusive)
            max_value: Maximum value (exclusive)

        Returns:
            Random integer in range
        """
        range_size = max_value - min_value
        num_bits = range_size.bit_length()
        num_bytes = (num_bits + 7) // 8

        while True:
            random_bytes = secrets.token_bytes(num_bytes)
            candidate = int.from_bytes(random_bytes, byteorder='big', signed=False)
            candidate = min_value + (candidate % range_size)

            if min_value <= candidate < max_value:
                return candidate

    @staticmethod
    def save_public_key(public_key: RSAPublicKey, file_path: Path) -> None:
        """Save RSA public key to file.

        Args:
            public_key: Public key to save
            file_path: Path to save file
        """
        logger.info("Saving public key to file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"{public_key.e}\n")
            f.write(f"{public_key.n}\n")

        logger.info("Public key saved successfully")

    @staticmethod
    def save_private_key(private_key: RSAPrivateKey, file_path: Path) -> None:
        """Save RSA private key to file.

        Args:
            private_key: Private key to save
            file_path: Path to save file
        """
        logger.info("Saving private key to file: %s", file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            f.write(f"{private_key.d}\n")
            f.write(f"{private_key.n}\n")

        logger.info("Private key saved successfully")

    @staticmethod
    def load_public_key(file_path: Path) -> RSAPublicKey:
        """Load RSA public key from file.

        Args:
            file_path: Path to load file from

        Returns:
            Public key loaded from file
        """
        logger.info("Loading public key from file: %s", file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Public key file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) < 2:
            raise ValueError("Invalid public key file format: expected at least 2 lines")

        e = int(lines[0].strip())
        n = int(lines[1].strip())

        logger.info("Public key loaded successfully")
        return RSAPublicKey(e=e, n=n)

    @staticmethod
    def load_private_key(file_path: Path) -> RSAPrivateKey:
        """Load RSA private key from file.

        Args:
            file_path: Path to load file from

        Returns:
            Private key loaded from file
        """
        logger.info("Loading private key from file: %s", file_path)

        if not file_path.exists():
            raise FileNotFoundError(f"Private key file not found: {file_path}")

        with file_path.open("r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) < 2:
            raise ValueError("Invalid private key file format: expected at least 2 lines")

        d = int(lines[0].strip())
        n = int(lines[1].strip())

        logger.info("Private key loaded successfully")
        return RSAPrivateKey(d=d, n=n)

