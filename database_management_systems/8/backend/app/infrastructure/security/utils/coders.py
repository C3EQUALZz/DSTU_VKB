import bcrypt
import jwt


def encode_jwt(
        payload: dict,
        private_key: str,
        algorithm: str,
) -> str:
    return jwt.encode(
        payload=payload,
        private_key=private_key,
        algorithm=algorithm,
    )


def decode_jwt(
        token: str | bytes,
        public_key: str,
        algorithm: str
) -> str:
    decoded = jwt.decode(
        token,
        public_key,
        algorithms=[algorithm],
    )
    return decoded


def hash_password(
        password: str,
) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(
        password: str,
        hashed_password: str,
) -> bool:
    return bcrypt.checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode(),
    )
