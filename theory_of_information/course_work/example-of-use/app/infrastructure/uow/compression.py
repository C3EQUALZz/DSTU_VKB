from app.infrastructure.uow.base import AbstractUnitOfWork


class CompressionUnitOfWork(AbstractUnitOfWork):
    """
    Interface for any units of work, which would be used for transaction atomicity, according DDD.
    """

    async def commit(self) -> None:
        raise NotImplementedError

    async def rollback(self) -> None:
        raise NotImplementedError
