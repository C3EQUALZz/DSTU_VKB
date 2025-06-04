"""
Для полученных рядов (t1, t2) посчитать основные статистические показатели - мат. ожидание,
дисперсию, СКО и оценить полученные результаты.
"""

from pathlib import Path
import pandas as pd
import numpy as np


def solve(*paths: Path) -> None:
    """
    Функция считывает CSV-файлы с временем выполнения запросов
    и выводит основные статистические показатели: мат. ожидание, дисперсию, СКО.

    :param paths: Пути к CSV-файлам.
    """

    if not all(path.exists() for path in paths):
        raise FileNotFoundError("Не все указанные файлы существуют.")

    if not all(path.suffix.lower() == ".csv" for path in paths):
        raise ValueError("Все файлы должны быть формата .csv")

    for path in paths:
        try:
            df = pd.read_csv(path)

            if "duration_sec" not in df.columns:
                raise ValueError(f"Файл {path} не содержит колонки 'duration_sec'")

            durations = df["duration_sec"].values

            mean_time = np.mean(durations)
            variance = np.var(durations)
            std_dev = np.std(durations)

            print(f"\n📊 Статистика для файла: {path.name}")
            print("-" * 40)
            print(f"🔢 Количество измерений: {len(durations)}")
            print(f"🧮 Математическое ожидание: {mean_time:.6f} сек.")
            print(f"📉 Дисперсия: {variance:.10f}")
            print(f"📉 Стандартное отклонение (СКО): {std_dev:.10f}")
            print("-" * 40)

        except Exception as e:
            raise RuntimeError(f"Ошибка при обработке файла {path}: {e}")