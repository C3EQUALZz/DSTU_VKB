import asyncio

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker, AsyncSession

from app.application.solve import pipeline
from app.settings.app import Settings


async def main() -> None:
    settings: Settings = Settings()

    engine: AsyncEngine = create_async_engine(
        url=settings.database.url,
        pool_pre_ping=settings.alchemy.pool_pre_ping,
        pool_recycle=settings.alchemy.pool_recycle,
        echo=settings.alchemy.echo,
    )

    session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        autoflush=settings.alchemy.auto_flush,
        expire_on_commit=settings.alchemy.expire_on_commit,
    )

    await pipeline(session_maker)


if __name__ == "__main__":
    asyncio.run(main())