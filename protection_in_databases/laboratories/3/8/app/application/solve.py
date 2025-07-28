import time
from typing import Tuple, Dict, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def pipeline(async_session_maker: async_sessionmaker[AsyncSession]) -> None:
    """Основной пайплайн обработки данных для задания 8"""
    start_total_time = time.perf_counter()

    # Выполняем запрос с группировкой
    group_by_results, execution_time = await execute_group_by_query(async_session_maker)

    total_time = time.perf_counter() - start_total_time

    # Вывод результатов
    print("\nРезультаты обработки (GROUP BY):")
    print("-" * 60)
    print(f"{'Год':<10} | {'Кол-во оценок':<15} | {'Время (сек)':<12}")
    print("-" * 60)

    for year, count in sorted(group_by_results.items()):
        year_str = str(year) if year is not None else "NULL"
        count_str = str(count)
        print(f"{year_str:<10} | {count_str:<15} | {execution_time:.6f}")

    print("-" * 60)
    print(f"ОБЩЕЕ ВРЕМЯ ВЫПОЛНЕНИЯ: {total_time:.6f} секунд")
    print(f"Время выполнения GROUP BY запроса: {execution_time:.6f} секунд")
    print(f"Обработано лет: {len(group_by_results)}")


async def execute_group_by_query(
        async_session_maker: async_sessionmaker[AsyncSession]
) -> Tuple[Dict[Any, int], float]:
    """Выполнение запроса с группировкой по году"""
    start_time = time.perf_counter()

    async with async_session_maker() as session:
        # Выполняем запрос с группировкой
        query = text("""
            SELECT plyear, COUNT(id) 
            FROM istudents.mark 
            WHERE value > 40 AND plyear IS NOT NULL
            GROUP BY plyear
        """)
        result = await session.execute(query)
        rows = result.all()

    execution_time = time.perf_counter() - start_time

    # Преобразуем результаты в словарь {год: количество}
    group_by_results = {}
    for row in rows:
        year, count = row
        group_by_results[year] = count

    return group_by_results, execution_time
