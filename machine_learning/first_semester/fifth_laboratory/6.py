"""
В датафрейме transactions задайте столбец customer_id в качестве индекса.
Выделите клиента с максимальной суммой транзакции (то есть с максимальным приходом на карту). (*)
"""

import zipfile

import pandas as pd


def read_data(zip_filepath: str, csv_filename: str, index_col: str = "customer_id") -> pd.DataFrame:
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        with zip_ref.open(csv_filename, 'r') as f:
            return pd.read_csv(f, sep=',', index_col=index_col)


def get_the_client_with_max_transaction(dataframe: pd.DataFrame):
    dataframe = dataframe.groupby('customer_id')['amount'].max()
    return dataframe[dataframe == dataframe.max()]


def main() -> None:
    zip_filepath = 'data.zip'
    csv_filename = 'data/transactions.csv'

    df = read_data(zip_filepath, csv_filename)

    client = get_the_client_with_max_transaction(df)

    print(
        "Наш датафрейм: ", df,
        "Клиент с максимальной суммой транзакции", client,
        sep="\n\n"
    )


if __name__ == '__main__':
    main()
