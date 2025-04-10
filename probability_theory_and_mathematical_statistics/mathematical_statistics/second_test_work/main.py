"""
Выполнил Ковалев Данил ВКБ22.

Запрещено использовать сторонние библиотеки, которые предназначены для математических операций.

- seaborn, matplotlib - это библиотеки, которые предназначены для отрисовки функций.
- Collections - встроенный словарь, который быстро подсчитывает элементы и число их вхождений.

Набор данных, который использовался:

- https://www.kaggle.com/datasets/subhajournal/wine-quality-data-combined
"""

from collections import Counter

import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes


class DataInteraction:
    def __init__(
        self,
        data: list[float],
        indices: slice,
        comment: str,
        *,
        chart_histogram: bool = True,
        chart_frequency_range: bool = True,
    ) -> None:
        self.data = data[indices]
        self.comment = comment
        self.chart_histogram = chart_histogram
        self.chart_frequency_range = chart_frequency_range
        self._draw()

    def _calculate_variation_series(self) -> list[float]:
        """
        Здесь создается вариационный ряд
        """
        return sorted(self.data)

    def _calculate_average_selection(self) -> float:
        """
        Здесь подсчитывается среднее значение выборки.
        Зависит все от данных.
        """
        return sum(self.data) / len(self.data)

    def _calculate_dispersion(self) -> float:
        """
        Подсчет дисперсии выборки
        """
        average = self._calculate_average_selection()
        return sum(map(lambda x: (x - average) ** 2, self.data)) / len(self.data)

    def _calculate_standard_deviation(self) -> float:
        """
        Подсчет стандартного отклонения выборки
        """
        return self._calculate_dispersion() ** 0.5

    def _calculate_dispersion_corrected(self) -> float:
        """
        Подсчет дисперсии исправленной
        """
        average = self._calculate_average_selection()
        return sum(map(lambda x: (x - average) ** 2, self.data)) / (len(self.data) - 1)

    def _calculate_standard_deviation_corrected(self) -> float:
        """
        Подсчет исправленного стандартного отклонения
        """
        return self._calculate_dispersion_corrected() ** 0.5

    def _draw(self) -> None:
        """
        Здесь происходит отрисовка графиков
        """
        if not self.chart_histogram and not self.chart_frequency_range:
            return

        fig, axes = plt.subplots(
            1, self.chart_frequency_range + self.chart_histogram, figsize=(12, 6)
        )

        if isinstance(axes, Axes):
            axes = [axes]

        i = 0
        titles = []

        if self.chart_histogram:
            sns.histplot(self.data, bins=25, ax=axes[i])
            titles.append(f"Гистограмма '{self.comment}'")
            axes[i].set_xlabel("Значения выборки")
            axes[i].set_ylabel("Высота")
            i += 1

        if self.chart_frequency_range:
            data_frequency = Counter(self.data)
            sns.lineplot(x=data_frequency.keys(), y=data_frequency.values(), ax=axes[i])
            titles.append(f"Полигон частот '{self.comment}'")
            axes[i].set_xlabel("Значения выборки")
            axes[i].set_ylabel("Количество совпадений")
            i += 1

        for ax, title in zip(axes, titles):
            ax.set_title(title)
            ax.set_xlim(left=0)
            ax.set_ylim(bottom=0)

        plt.savefig(f"{'_'.join(self.comment.split())}.png")
        plt.show()

    @staticmethod
    def __pretty_print(data: list[float]) -> str:
        """
        Статический метод для красивого вывода списка на экран
        """
        sub_lists = (data[i : i + 10] for i in range(0, len(data), 10))
        aligned_sublist = (
            " ".join(f"{item:<5}" for item in sub_list) for sub_list in sub_lists
        )
        return "\n".join(aligned_sublist)

    def __str__(self) -> str:
        result = (
            f"{self.comment}:\n{self.__pretty_print(self.data)}\n\n"
            f"Вариационный ряд:\n{self.__pretty_print(self._calculate_variation_series())}\n\n"
            f"Среднее значение '{self.comment}': {self._calculate_average_selection()}\n\n"
            f"Дисперсия '{self.comment}': {self._calculate_dispersion()}\n\n"
            f"Стандартное отклонение '{self.comment}': {self._calculate_standard_deviation()}\n\n"
        )

        if self.comment != "Генеральная совокупность":
            result += (
                f"Дисперсия испр. '{self.comment}': {self._calculate_dispersion_corrected()}\n\n"
                f"Стандартное отклонение испр. '{self.comment}': {self._calculate_standard_deviation_corrected()}\n\n"
            )

        return result


def main() -> None:
    """
    Точка запуска логики
    """
    with open("data/dataset.txt", mode="r", encoding="utf-8") as file:
        data: list[float] = list(map(float, file.readlines()))

        questions = (
            DataInteraction(
                data,
                slice(0, len(data)),
                "Генеральная совокупность",
                chart_histogram=True,
                chart_frequency_range=True,
            ),
            DataInteraction(
                data,
                slice(0, len(data), 2),
                "Выборка из ГС через 1 элемент",
                chart_histogram=True,
                chart_frequency_range=False,
            ),
            DataInteraction(
                data,
                slice(1, len(data), 4),
                "Выборка из ГС через 3 элемента, начиная с 1",
                chart_histogram=False,
                chart_frequency_range=True,
            ),
            DataInteraction(
                data,
                slice(3, len(data), 2),
                "Аудиторная часть",
                chart_histogram=True,
                chart_frequency_range=True,
            ),
        )

        for number, question in enumerate(filter(None, questions), start=1):
            print(f"{str(number) + ' Задание':-^60}\n")
            print(question)


if __name__ == "__main__":
    main()
