"""
Выполнить выборку данных (30 раз с различными условиями,
фильтрация по полю tmark_fk - условия могут циклически повторяться) - замерить время - получим ряд t1;
"""
import asyncio
import csv
import time
from random import randint
from typing import Iterable, Generator, Coroutine

from sqlalchemy import text, TextClause
from sqlalchemy.ext.asyncio import AsyncEngine

from app.settings.app import get_settings, Settings


async def first_question(
        engine: AsyncEngine,
        times: int = 30
) -> None:
    """
    Точка запуска выполнения подзадания a из задания 3.
    Здесь нужно проверить сколько по времени будут выполняться запросы с определенными условиями.
    :param engine: Движок для подключения к базе данных.
    :param times: Количество раз сколько нужно выполнить запрос к базе.
    :return:
    """
    settings: Settings = get_settings()

    select_query: TextClause = text("SELECT * FROM istudents.mark WHERE tmark_fk = :fk")

    marks: list[int] = [randint(1, 500) for _ in range(times)]

    # Передаём mark вместе с query
    coroutines: Generator[Coroutine[AsyncEngine, TextClause, float], None, None] = (
        execute_query(engine, select_query, mark)
        for mark in marks
    )

    durations: Iterable[float] = await asyncio.gather(*coroutines)

    # Сохраняем в CSV
    with open(settings.performance.select_benchmark, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["query_number", "tmark_fk", "duration_sec"])

        for mark, (i, duration) in zip(marks, enumerate(durations)):
            writer.writerow([i + 1, mark, duration])

    print(f"✅ Результаты сохранены в {settings.performance.select_benchmark}")


async def execute_query(
        engine: AsyncEngine,
        query: TextClause,
        mark: int
) -> float:
    start: float = time.perf_counter()

    async with engine.connect() as conn:
        await conn.execute(query, {"fk": mark})

    return time.perf_counter() - start
