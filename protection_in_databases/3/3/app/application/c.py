"""
Измерения t1, t2 представить на графиках - объяснить их форму;
"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
from pandas import DataFrame


def solve(
        *paths: Path,
) -> None:
    """
    Функция для построения графиков исходя из требований к заданию.
    :param paths: Пути к файлам, которые мы хотим построить.
    """
    if not all(path.exists() for path in paths):
        raise RuntimeError("Сначала прогоните результаты измерений, запустив пункты `a` и `b`")

    if not all(path.suffix.lower() == ".csv" for path in paths):
        raise ValueError("Все файлы должны быть формата .csv")

    for path in paths:
        try:
            df: DataFrame = pd.read_csv(path)

            # Предположим, что в CSV есть колонки "query_number" и "duration_sec"
            x = df["query_number"]
            y = df["duration_sec"]

            plt.figure(figsize=(10, 6))
            plt.plot(x, y, marker="o", linestyle="-", label=f"{path.stem}")

            plt.title(f"График производительности: {path.name}")
            plt.xlabel("Номер запроса")
            plt.ylabel("Время выполнения (сек)")
            plt.grid(True)
            plt.tight_layout()
            plt.legend()
            plt.show()

        except KeyError as e:
            raise ValueError(f"Файл {path} не содержит необходимных данных: {e}")