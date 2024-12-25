from datetime import (
    datetime,
    timedelta,
    UTC,
)

import jwt
from app.infrastructure.exceptions import (
    ExpiredToken,
    InvalidToken,
)
from app.infrastructure.security.cookies.base import BaseCookieTokenManager


class PyJWTCookieTokenManager(BaseCookieTokenManager):
    async def create_access_token(self, user_oid: str) -> str:
        to_encode = {
            "sub": user_oid,
            "exp": datetime.now(UTC) + timedelta(minutes=self._access_token_expire_minutes),
        }
        return jwt.encode(to_encode, self._token_secret_key, algorithm=self._algorithm)

    async def create_refresh_token(self, user_oid: str) -> str:
        to_encode = {
            "sub": user_oid,
            "exp": datetime.now(UTC) + timedelta(days=self._refresh_token_expire_days),
        }
        return jwt.encode(to_encode, self._token_secret_key, algorithm=self._algorithm)

    async def get_payload(self, token: str) -> str:
        try:
            payload: dict = jwt.decode(token, self._token_secret_key, algorithms=[self._algorithm])
            user_oid = payload.get("sub")

        except jwt.ExpiredSignatureError:
            raise ExpiredToken

        except jwt.DecodeError:
            raise InvalidToken

        return user_oid
