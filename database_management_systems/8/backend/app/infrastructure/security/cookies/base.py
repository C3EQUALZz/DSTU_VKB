from abc import ABC

from app.infrastructure.security.base import BaseTokenManger


class BaseCookieTokenManager(BaseTokenManger, ABC):
    ...
