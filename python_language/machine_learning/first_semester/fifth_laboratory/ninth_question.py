"""
Создайте новый столбец - mcc_code+tr_type, сконкатенировав значения из соответствующих столбцов. (*)
Оставьте только наблюдения с отрицательным значением amount.
"""

import zipfile

import pandas as pd


def read_data(zip_filepath: str, csv_filename: str, sep: str = ",") -> pd.DataFrame:
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        with zip_ref.open(csv_filename) as f:
            return pd.read_csv(f, sep=sep)


def execute(
        transactions: pd.DataFrame,
        tr_mcc_codes: pd.DataFrame,
        tr_types: pd.DataFrame,
        gender_train: pd.DataFrame,
) -> pd.DataFrame:
    df = pd.merge(transactions, gender_train, how='left')
    df = pd.merge(pd.merge(df, tr_types, how='inner'), tr_mcc_codes, how='inner')
    df['mcc_code+tr_type'] = df['mcc_code'].astype(str) + df['tr_type'].astype(str)
    return df[df['amount'] < 0]


def main() -> None:
    files = (
        ("data.zip", "data/transactions.csv", ","),
        ("data.zip", "data/tr_mcc_codes.csv", ";"),
        ("data.zip", "data/tr_types.csv", ";"),
        ("data.zip", "data/gender_train.csv", ","),
    )

    frames = []

    for file in files:
        frame = read_data(*file)
        print(f"Файл с именем {file[1]}. Значения: ", frame, sep="\n\n")
        frames.append(frame)

    print(f"Новый столбец mcc_code+tr_type: ", execute(*frames), sep="\n\n")


if __name__ == "__main__":
    main()
