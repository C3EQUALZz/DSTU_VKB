import asyncio

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from app.application.a import solve as first_question
from app.settings.app import Settings


def main() -> None:
    settings: Settings = Settings()

    settings.performance.select_benchmark.parent.mkdir(exist_ok=True, parents=True)

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

    while True:
        choice: str = input("Введите задание для выбора: a, b, c, d. Для выхода введите 'exit'")

        if choice.lower().strip() == "exit":
            exit(0)

        match choice:
            case "a":
                asyncio.run(
                    first_question(
                        session_maker=session_maker,
                        path_to_select_benchmark_result=settings.performance.select_benchmark
                    )
                )

            case "b":
                ...

            case "c":
                ...

            case "d":
                ...

            case _:
                print("Неверный вариант для выбора. Перезапускаю! ")


if __name__ == "__main__":
    main()
