"""
Выполнил Ковалев Данил ВКБ22.

Запрещено использовать сторонние библиотеки, которые предназначены для математических операций.

- seaborn, matplotlib - это библиотеки, которые предназначены для отрисовки функций.

Набор данных, который использовался:

- https://www.kaggle.com/datasets/subhajournal/wine-quality-data-combined
"""
import seaborn as sns

from matplotlib.axes import Axes
from matplotlib import pyplot as plt


class DataInteraction:
    def __init__(self, data: list[float], indices: tuple[int, ...], comment: str,
                 *, chart_histogram: bool = True, chart_frequency_range: bool = True,
                 ) -> None:

        self.data = [data[i] for i in range(len(data)) if i % 10 in indices]
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
        fig, axes = plt.subplots(1, self.chart_frequency_range + self.chart_histogram, figsize=(12, 6))

        if isinstance(axes, Axes):
            axes = [axes]

        i = 0
        titles = []

        if self.chart_histogram:
            sns.histplot(self.data, bins=25, ax=axes[i])
            titles.append(f"Гистограмма '{self.comment}'")
            i += 1

        if self.chart_frequency_range:
            sns.kdeplot(self.data, bw_adjust=0.1, ax=axes[i])
            titles.append(f"Полигон частот '{self.comment}'")
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
        sub_lists = (data[i:i + 10] for i in range(0, len(data), 10))
        aligned_sublist = (" ".join(f"{item:<5}" for item in sub_list) for sub_list in sub_lists)
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
    with open("dataset.txt", mode="r", encoding="utf-8") as file:
        data: list[float] = list(map(float, file.readlines()))

        questions = (
            DataInteraction(data, (0, 1, 2, 3, 4, 5, 6, 7, 8, 9), "Генеральная совокупность",
                            chart_histogram=True, chart_frequency_range=True),

            DataInteraction(data, (0, 2, 4, 6, 8), "Выборка из ГС через 1 элемент",
                            chart_histogram=True, chart_frequency_range=False),

            DataInteraction(data, (1, 5), "Выборка из ГС по желанию В.М",
                            chart_histogram=False, chart_frequency_range=True),
        )

        for number, question in enumerate(questions, start=1):
            print(f"{str(number) + ' Задание':-^60}\n")
            print(question)


if __name__ == "__main__":
    main()
