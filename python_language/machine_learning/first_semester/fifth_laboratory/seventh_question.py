"""
Соедините transactions с всеми остальными таблицами (tr_mcc_codes, tr_types, gender_train).
Причём с customers_gender_train необходимо смёрджиться с помощью left join, а с оставшимися датафреймами - через inner.

В результате соединения датафреймов должно получиться 999584 строки.
"""
import pandas as pd
import zipfile


def read_data(zip_filepath: str, csv_filename: str, sep: str = ",") -> pd.DataFrame:
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        with zip_ref.open(csv_filename, 'r') as f:
            return pd.read_csv(f, sep=sep)


def merge_pandas_frames(
        transactions: pd.DataFrame,
        tr_mcc_codes: pd.DataFrame,
        tr_types: pd.DataFrame,
        gender_train: pd.DataFrame
) -> pd.DataFrame:
    df = pd.merge(transactions, gender_train, how='left')
    return pd.merge(pd.merge(df, tr_types, how='inner'), tr_mcc_codes, how='inner')


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

    df = merge_pandas_frames(
        *frames
    )

    print("В результате слияний получилось: ", df, sep="\n\n")


if __name__ == '__main__':
    main()
