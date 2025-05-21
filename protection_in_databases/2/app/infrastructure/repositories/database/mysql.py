from abc import ABC

from pymysql import Connection

from app.infrastructure.repositories.database.base import AbstractRepository


class PyMySQLAbstractRepository(AbstractRepository, ABC):
    """
    Repository interface for SQLAlchemy, from which should be inherited all other repositories,
    which would be based on SQLAlchemy logics.
    """

    def __init__(self, connection: Connection) -> None:
        self._connection: Connection = connection
