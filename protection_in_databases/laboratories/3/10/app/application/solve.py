import asyncio
import time
from collections import deque
from typing import Coroutine, Any, Final

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

ITERATIONS: Final[int] = 30
LIMIT: Final[int] = 100


async def pipeline(async_session_maker: async_sessionmaker[AsyncSession]) -> None:
    """Основной пайплайн обработки данных для задания 10"""
    start_total_time: float = time.perf_counter()

    # Параметры выполнения
    execution_times: deque[float] = deque()
    total_rows: int = 0

    # Создаем задачи для параллельного выполнения
    tasks: deque[Coroutine[Any, Any, tuple[int, float]]] = deque()
    for i in range(ITERATIONS):
        offset: int = i * LIMIT
        tasks.append(execute_query(async_session_maker, LIMIT, offset))

    # Запускаем все задачи параллельно
    results = await asyncio.gather(*tasks)

    # Обработка результатов
    for i, (rows, exec_time) in enumerate(results):
        execution_times.append(exec_time)
        total_rows += len(rows)
        print(f"Итерация {i + 1}: получено {len(rows)} строк, время: {exec_time:.6f} сек")

    total_time = time.perf_counter() - start_total_time

    # Статистика
    avg_time: float = sum(execution_times) / len(execution_times)
    min_time: float = min(execution_times)
    max_time: float = max(execution_times)

    # Вывод результатов
    print("\nРезультаты обработки:")
    print("-" * 70)
    print(f"Всего итераций: {ITERATIONS}")
    print(f"Всего получено строк: {total_rows}")
    print(f"Общее время выполнения: {total_time:.6f} секунд")
    print(f"Среднее время на итерацию: {avg_time:.6f} сек")
    print(f"Минимальное время: {min_time:.6f} сек")
    print(f"Максимальное время: {max_time:.6f} сек")
    print("-" * 70)

    # Вывод времени каждой итерации
    print("\nВремя выполнения по итерациям:")
    for i, t in enumerate(execution_times):
        print(f"Итерация {i + 1}: {t:.6f} сек")


async def execute_query(
        async_session_maker: async_sessionmaker[AsyncSession],
        limit: int,
        offset: int
) -> tuple[int, float]:
    start_time = time.perf_counter()

    async with async_session_maker() as session:
        query = text("""
            SELECT mark.*, studplan.* 
            FROM istudents.mark 
            INNER JOIN istudents.studplan 
                ON mark.studplan_fk = studplan.id
            LIMIT :limit OFFSET :offset
        """)

        result = await session.execute(query, {"limit": limit, "offset": offset})
        rows = result.fetchall()

    exec_time = time.perf_counter() - start_time

    return rows, exec_time
