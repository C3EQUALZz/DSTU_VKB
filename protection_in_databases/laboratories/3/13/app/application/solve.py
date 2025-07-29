import asyncio
import statistics
import time
from collections import deque
from typing import List, Tuple, Deque

from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

# Константы
ITERATIONS = 30
LIMIT = 100


async def execute_query(
        async_session_maker: async_sessionmaker[AsyncSession],
        limit: int,
        offset: int
) -> Tuple[int, int, float]:
    """Выполнение одного запроса с замером времени"""
    start_time = time.perf_counter()
    try:
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
            return offset, len(rows), time.perf_counter() - start_time
    except Exception as e:
        print(f"Ошибка при выполнении запроса (offset={offset}): {e}")
        return offset, 0, time.perf_counter() - start_time


async def pipeline(async_session_maker: async_sessionmaker[AsyncSession]) -> None:
    """Основной пайплайн обработки данных для задания 11 с параллельным выполнением"""
    start_total_time: float = time.perf_counter()

    # Создаем задачи для параллельного выполнения
    tasks = []
    for i in range(ITERATIONS):
        offset = i * LIMIT
        tasks.append(execute_query(async_session_maker, LIMIT, offset))

    # Выполняем все запросы параллельно
    results = await asyncio.gather(*tasks)

    # Собираем результаты
    execution_times: Deque[float] = deque()
    total_rows = 0
    sorted_results = sorted(results, key=lambda x: x[0])  # Сортируем по offset

    for i, (offset, row_count, exec_time) in enumerate(sorted_results):
        execution_times.append(exec_time)
        total_rows += row_count
        print(f"Итерация {i + 1:>2} (offset={offset:>4}): "
              f"получено {row_count:>3} строк, время: {exec_time:.6f} сек")

    total_time = time.perf_counter() - start_total_time

    # Статистический анализ (остается без изменений)
    if execution_times:
        avg_time = statistics.mean(execution_times)
        min_time = min(execution_times)
        max_time = max(execution_times)
        median_time = statistics.median(execution_times)
        stdev_time = statistics.stdev(execution_times) if len(execution_times) > 1 else 0.0

        # Вычисление процентилей
        sorted_times = sorted(execution_times)
        percentile_90 = sorted_times[int(len(sorted_times) * 0.9)]
        percentile_95 = sorted_times[int(len(sorted_times) * 0.95)]
        percentile_99 = sorted_times[int(len(sorted_times) * 0.99)]

        # Коэффициент вариации
        cv = (stdev_time / avg_time) * 100 if avg_time > 0 else 0.0

        # Разница между max и min
        range_diff = max_time - min_time
    else:
        avg_time = min_time = max_time = median_time = stdev_time = 0.0
        percentile_90 = percentile_95 = percentile_99 = cv = range_diff = 0.0

    # Вывод результатов (остается без изменений)
    print("\n" + "=" * 80)
    print("СТАТИСТИЧЕСКИЙ АНАЛИЗ РЕЗУЛЬТАТОВ")
    print("=" * 80)
    print(f"{'Всего итераций:':<30} {ITERATIONS}")
    print(f"{'Всего получено строк:':<30} {total_rows}")
    print(f"{'Общее время выполнения:':<30} {total_time:.6f} секунд")
    print("-" * 80)

    print("\nОСНОВНЫЕ ПОКАЗАТЕЛИ:")
    print(f"{'Среднее время:':<25} {avg_time:.6f} сек")
    print(f"{'Медианное время:':<25} {median_time:.6f} сек")
    print(f"{'Минимальное время:':<25} {min_time:.6f} сек")
    print(f"{'Максимальное время:':<25} {max_time:.6f} сек")
    print(f"{'Размах (max-min):':<25} {range_diff:.6f} сек")
    print(f"{'Стандартное отклонение:':<25} {stdev_time:.6f} сек")
    print(f"{'Коэффициент вариации:':<25} {cv:.2f}%")

    print("\nПРОЦЕНТИЛИ:")
    print(f"{'90-й процентиль:':<25} {percentile_90:.6f} сек")
    print(f"{'95-й процентиль:':<25} {percentile_95:.6f} сек")
    print(f"{'99-й процентиль:':<25} {percentile_99:.6f} сек")

    print("\nДОПОЛНИТЕЛЬНАЯ ИНФОРМАЦИЯ:")
    print(f"{'Общее время / Итераций:':<25} {total_time / ITERATIONS:.6f} сек/итерация")
    print(f"{'Время на 100 строк:':<25} {total_time / total_rows * 100 if total_rows else 0:.6f} сек/100строк")
    print(f"{'Параллельный прирост:':<25} {sum(execution_times) / total_time:.2f}x")
    print("=" * 80)

    # Вывод времени каждой итерации
    print("\nДЕТАЛИЗАЦИЯ ПО ИТЕРАЦИЯМ:")
    for i, t in enumerate(execution_times):
        deviation = ((t - avg_time) / avg_time * 100) if avg_time > 0 else 0
        print(f"Итерация {i + 1:>2}: {t:.6f} сек ({deviation:+.2f}%)")