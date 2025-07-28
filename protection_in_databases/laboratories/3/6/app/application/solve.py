import asyncio
import time
from typing import List, Tuple, Any

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


async def pipeline(async_session_maker: async_sessionmaker[AsyncSession]):
    """Основной пайплайн обработки данных"""
    start_total_time = time.perf_counter()

    # Получение уникальных годов (исключая NULL)
    years = await get_unique_years(async_session_maker)
    print(f"Найдено {len(years)} уникальных годов")

    # Асинхронная обработка каждого года
    tasks = [process_year(async_session_maker, year) for year in years]
    results = await asyncio.gather(*tasks)

    # Фильтрация и преобразование результатов
    valid_results: List[Tuple[Any, Any, float]] = []
    for item in results:
        year, count, exec_time = item

        # Преобразование None в 0 для count
        if count is None:
            count = 0

        # Преобразование года в строку (для безопасного форматирования)
        year_str = str(year) if year is not None else "NULL"
        valid_results.append((year_str, count, exec_time))

    # Сортировка по году для лучшей читаемости
    valid_results.sort(key=lambda x: x[0])

    total_time: float = time.perf_counter() - start_total_time

    # Вывод результатов
    print("\nРезультаты обработки:")
    print("-" * 60)
    print(f"{'Год':<10} | {'Кол-во оценок':<15} | {'Время (сек)':<12}")
    print("-" * 60)

    for year, count, exec_time in valid_results:
        print(f"{year:<10} | {count:<15} | {exec_time:.6f}")

    print("-" * 60)
    print(f"ОБЩЕЕ ВРЕМЯ ВЫПОЛНЕНИЯ: {total_time:.6f} секунд")
    print(f"Обработано лет: {len(valid_results)}")

    # Защита от деления на ноль
    if valid_results:
        avg_time = total_time / len(valid_results)
        min_time = min(t for _, _, t in valid_results)
        max_time = max(t for _, _, t in valid_results)

        print(f"Среднее время на год: {avg_time:.6f} сек")
        print(f"Минимальное время: {min_time:.6f} сек")
        print(f"Максимальное время: {max_time:.6f} сек")
    else:
        print("Нет данных для расчета статистики времени")

    return valid_results


async def get_unique_years(async_session_maker: async_sessionmaker[AsyncSession]) -> List[int]:
    """Получение уникальных годов из таблицы (исключая NULL)"""
    async with async_session_maker() as session:
        query = text("SELECT DISTINCT plyear FROM istudents.mark WHERE plyear IS NOT NULL")
        result = await session.execute(query)
        return [row[0] for row in result.all()]


async def process_year(
        async_session_maker: async_sessionmaker[AsyncSession],
        year: int
) -> Tuple[int, int, float]:
    """Обработка данных для конкретного года"""
    start_time: float = time.perf_counter()

    async with async_session_maker() as session:
        query = text("""
            SELECT COUNT(*) 
            FROM istudents.mark 
            WHERE value > 40 AND plyear = :year
        """)
        result = await session.execute(query, {"year": year})

        # Безопасное получение результата
        count = result.scalar_one_or_none()
        if count is None:
            count = 0

    execution_time: float = time.perf_counter() - start_time

    return year, count, execution_time