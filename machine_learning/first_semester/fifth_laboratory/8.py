"""
Определите модуль разницы между средними тратами женщин и мужчин (трата - отрицательное значение amount).

Выведите ответ в виде вещественного числа, округлённого до двух знаков после запятой,
отделив дробную часть точкой в формате "123.45".

Пояснения:
Если в результате для мужчин получились значения [-1,-3,-5], а для женщин [-1,-2,-3],
то модуль разницы между средними арифметическими -3 и -2 будет равен 1.
"""
import zipfile
import pandas as pd


def read_data(zip_filepath: str, csv_filename: str, sep: str = ",") -> pd.DataFrame:
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        with zip_ref.open(csv_filename) as f:
            return pd.read_csv(f, sep=sep)


def calculate_average_expense(df: pd.DataFrame, gender: float) -> float:
    gender_expenses = df[(df['gender'] == gender) & (df['amount'] < 0)]['amount']
    return gender_expenses.mean()


def execute(transactions: pd.DataFrame, gender_train: pd.DataFrame) -> float:
    df = pd.merge(transactions, gender_train, how='left')

    avg_male_expense = calculate_average_expense(df, gender=1.0)
    avg_female_expense = calculate_average_expense(df, gender=0.0)

    return round(abs(avg_female_expense - avg_male_expense), 2)


def main() -> None:
    files = [
        ("data.zip", "data/transactions.csv"),
        ("data.zip", "data/gender_train.csv")
    ]

    frames = []

    for file in files:
        frame = read_data(*file)
        print(f"Файл с именем {file[1]}. Значения: ", frame, sep="\n\n")
        frames.append(frame)

    result = execute(*frames)

    print(f"Модуль разницы между средними тратами женщин и мужчин: {result}")


if __name__ == "__main__":
    main()
