"""
1. В tr_types выберите произвольные 100 строк с помощью метода sample (указав при этом random_seed равный 242)
2. В полученной на предыдущем этапе подвыборке найдите долю наблюдений (стобец tr_description),
в которой содержится подстрока 'плата' (в любом регистре).

Выведите ответ в виде вещественного числа, округлённого до двух знаков после запятой,
отделив дробную часть точкой в формате "123.45"

Пояснения:
Строки "ПлатА за аренду",
"ПлатАза аренду",
"ПЛАТА" удовлетворяют условию, так как будучи переведёнными в нижний регистр содержат подстроку "плата".
"""

import numpy as np
import pandas as pd
import zipfile

np.random.seed(242)


def read_data(zip_filepath: str, csv_filename: str) -> pd.DataFrame:
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        with zip_ref.open(csv_filename, 'r') as f:
            return pd.read_csv(f, sep=';')


def sample_and_calculate_ratio(df: pd.DataFrame, sample_size: int, substring: str) -> float:
    sampled_df = df.sample(sample_size)
    count_with_substring = sampled_df.loc[sampled_df.tr_description.str.lower().str.contains(substring)].shape[0]
    ratio = count_with_substring / sample_size
    return round(ratio, 2)


def main() -> None:
    zip_filepath = 'data.zip'
    csv_filename = 'data/tr_types.csv'
    sample_size = 100
    substring = 'плата'

    df = read_data(zip_filepath, csv_filename)
    print("Датафрейм: ", df, sep='\n')
    ratio = sample_and_calculate_ratio(df, sample_size, substring)
    print(f"Доля наблюдений слова {substring} равна {ratio:.2f}")


if __name__ == "__main__":
    main()
