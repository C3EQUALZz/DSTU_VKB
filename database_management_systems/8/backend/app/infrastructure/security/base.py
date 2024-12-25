from abc import (
    ABC,
    abstractmethod,
)


class BaseTokenManger(ABC):
    def __init__(
            self,
            token_secret_key: str,
            algorithm: str,
            access_token_expire_minutes: int,
            refresh_token_expire_days: int
    ) -> None:
        self._token_secret_key: str = token_secret_key
        self._algorithm: str = algorithm
        self._access_token_expire_minutes: int = access_token_expire_minutes
        self._refresh_token_expire_days: int = refresh_token_expire_days

    @abstractmethod
    async def create_access_token(self, user_oid: str) -> str:
        pass

    @abstractmethod
    async def create_refresh_token(self, user_oid: str) -> str:
        pass

    @abstractmethod
    async def get_payload(self, token: str) -> str:
        pass
