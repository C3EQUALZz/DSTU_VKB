"""
Функция F(x, y) задана следующим образом:

        { x - y, если x <= y
F(x,y) ={ x + y, если x > y

Вывести на экран в виде таблицы значения функции F(x, y) для значений аргументов x = 0,5 - 0,7 с шагом 0,1 и y = 0,2 - 1,0
с шагом 0,2.
"""


# Определяем функцию F(x, y)
def f(x: float, y: float) -> float:
    return x - y if x > y else x + y


def main() -> None:
    x_values: list[float] = [0.5, 0.6, 0.7]  # x: 0.5 → 0.7 с шагом 0.1
    y_values: list[float] = [0.2, 0.4, 0.6, 0.8, 1.0]  # y: 0.2 → 1.0 с шагом 0.2

    # Форматируем шапку таблицы
    header: str = " y \\ x  | " + " | ".join(f"{x:5}" for x in x_values)
    divider: str = "-" * len(header)

    # Выводим таблицу
    print(header, divider, sep="\n")

    for y in y_values:
        row: str = f" {y:4}   | " + " | ".join(f"{f(x, y):5.2f}" for x in x_values)
        print(row, divider, sep="\n")


if __name__ == "__main__":
    main()
