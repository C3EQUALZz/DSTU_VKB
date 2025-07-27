"""
Выполнить вставку данных (30 раз различные данные) - замерить время. Получить ряд t2.
"""
import asyncio
import csv
import time
from datetime import timedelta, datetime
from pathlib import Path
from typing import Generator, Coroutine, Mapping, Iterable, Awaitable
from random import randint
from sqlalchemy import TextClause, text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession, AsyncEngine


async def solve(
        session_maker: async_sessionmaker[AsyncSession],
        path_to_insert_benchmark_result: Path,
        times: int = 30
) -> None:
    """
    Здесь функция, которая запускает на выполнение вставку различных значений в таблицу 'istudents.mark`
    :param session_maker: Фабрика сессий для подключения к базе данных.
    :param path_to_insert_benchmark_result: Путь для сохранения измерений для таблицы.
    :param times: Количество раз сколько нужно выполнить запрос к базе.
    :return:
    """

    insert_query: TextClause = text(
        """
        INSERT INTO istudents.mark (
            tmark_fk,
            studplan_fk,
            value, 
            mdate,
            attendance,
            person_fk,
            date_lock,
            date_return
        )
        VALUES (
            :tmark_fk,
            :studplan_fk,
            :value,
            :mdate,
            :attendance,
            :person_fk,
            :date_lock,
            :date_return
        )
    """
    )

    coroutines: Generator[Awaitable[float], None, None] = (
        execute_query(
            session_maker(),
            insert_query,
            generate_random_values()
        )
        for _ in range(times)
    )

    durations: Iterable[float] = await asyncio.gather(*coroutines)

    with open(path_to_insert_benchmark_result, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query_number", "duration_sec"])
        for i, duration in enumerate(durations):
            writer.writerow([i + 1, duration])

    print(f"✅ Результаты сохранены в {path_to_insert_benchmark_result}")


def generate_random_values() -> Mapping[str, int | str]:
    """
    Генерирует случайные значения для вставки в таблицу istudents.mark.
    :return: Словарь с параметрами для запроса.
    """
    now = datetime.now()

    return {
        "tmark_fk": randint(1, 500),
        "studplan_fk": randint(1_000_000_000, 9_999_999_999),
        "value": randint(1, 100),
        "mdate": now - timedelta(days=randint(1, 365)),  # только дата
        "attendance": randint(0, 100),
        "person_fk": randint(1_000_000_000, 9_999_999_999),
        "date_lock": (now + timedelta(hours=randint(-24, 24))),
        "date_return": (now + timedelta(hours=randint(-24, 24)))
    }


async def execute_query(
        session: AsyncSession,
        query: TextClause,
        values: Mapping[str, int | str]
) -> float:
    """
    Выполняет SQL-запрос и замеряет время его выполнения.
    :param session: Асинхронная сессия SQLAlchemy.
    :param query: Текст SQL-запроса.
    :param values: Параметры для запроса.
    :return: Время выполнения запроса в секундах.
    """
    start_time: float = time.perf_counter()

    async with session:
        await session.execute(query, values)
        await session.commit()

    end_time: float = time.perf_counter()

    return end_time - start_time
