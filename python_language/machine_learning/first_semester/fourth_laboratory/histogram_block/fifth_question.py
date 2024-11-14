"""
5. Изобразите столбчатую диаграмму колонки «Класс жилья». Расположите в порядке убывания размеры столбцов.
В ответ запишите нужную последовательность цифр, например 1234 (начальные данные из ноута "Создание наглядных графиков")

Данные можно взять из ноута "Создание наглядных графиков"
"""
import matplotlib.pyplot as plt
import pandas as pd


def draw_histogram_by_param(data: pd.Series) -> None:
    plt.bar(data.index, data.values)
    plt.xticks(rotation=30, ha='right')
    plt.xlabel('Класс жилья')
    plt.ylabel('Число объявлений')
    plt.title('Распределение объявлений по классу жилья')
    plt.show()

    print('Порядок убывания размеров столбцов:', ''.join(map(str, data.index)))


def main() -> None:
    dataset = pd.read_csv('../housing_market_dataset.csv')
    type_counts = dataset['Класс жилья'].value_counts()
    type_counts = type_counts.sort_values(ascending=False)
    draw_histogram_by_param(type_counts)


if __name__ == '__main__':
    main()
