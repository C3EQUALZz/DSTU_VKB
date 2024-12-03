"""
1. Для поля tr_type датафрейма transactions посчитайте частоту встречаемости всех типов транзакций tr_type в transactions.
2. Из перечисленных вариантов выберите те, которые попали в топ-5 транзакций по частоте встречаемости.
"""
import zipfile

import pandas as pd


def read_data(zip_filepath: str, csv_filename: str) -> pd.DataFrame:
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        with zip_ref.open(csv_filename, 'r') as f:
            return pd.read_csv(f, sep=',')


def get_info_about_column(dataframe: pd.DataFrame, column_name: str) -> tuple[pd.Series, pd.Series]:
    tr_type_counts = dataframe[column_name].value_counts()
    top_5_tr_types = tr_type_counts.head(5).index.tolist()

    return tr_type_counts, top_5_tr_types


def main() -> None:
    zip_filepath = 'data.zip'
    csv_filename = 'data/transactions.csv'

    df = read_data(zip_filepath, csv_filename)
    info = get_info_about_column(df, column_name='tr_type')

    print(
        "Наш dataframe: ", df,
        "Частота встречаемости всех типов транзакций: ", info[0],
        'Топ-5 транзакций по частоте встречаемости: ', info[1],
        sep='\n\n'
    )


if __name__ == '__main__':
    main()
