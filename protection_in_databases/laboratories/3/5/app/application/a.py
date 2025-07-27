"""
Выполнить выборку данных (30 раз с различными условиями,
фильтрация по полю tmark_fk - условия могут циклически повторяться) - замерить время - получим ряд t1;
"""
import asyncio
import csv
import time
from pathlib import Path
from random import randint
from typing import Iterable, Generator, Awaitable

from sqlalchemy import text, TextClause
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def solve(
        session_maker: async_sessionmaker[AsyncSession],
        path_to_select_benchmark_result: Path,
        times: int = 30,
) -> None:
    """
    Точка запуска выполнения подзадания a из задания 3.
    Здесь нужно проверить сколько по времени будут выполняться запросы с определенными условиями.
    :param session_maker: Фабрика сессий для подключения к базе данных.
    :param path_to_select_benchmark_result: Путь для сохранения измерений для таблицы.
    :param times: Количество раз сколько нужно выполнить запрос к базе.
    :return:
    """

    select_query: TextClause = text("SELECT * FROM istudents.mark WHERE tmark_fk = :fk")

    marks: list[int] = [randint(0, 48) for _ in range(times)]

    coroutines: Generator[Awaitable[float], None, None] = (
        execute_query(session_maker(), select_query, mark)
        for mark in marks
    )

    durations: Iterable[float] = await asyncio.gather(*coroutines)

    # Сохраняем в CSV
    with open(path_to_select_benchmark_result, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query_number", "tmark_fk", "duration_sec"])

        for mark, (i, duration) in zip(marks, enumerate(durations)):
            writer.writerow([i + 1, mark, duration])

    print(f"✅ Результаты сохранены в {path_to_select_benchmark_result}")


async def execute_query(
        session: AsyncSession,
        query: TextClause,
        mark: int
) -> float:
    start: float = time.perf_counter()

    async with session:
        await session.execute(query, {"fk": mark})

    return time.perf_counter() - start
