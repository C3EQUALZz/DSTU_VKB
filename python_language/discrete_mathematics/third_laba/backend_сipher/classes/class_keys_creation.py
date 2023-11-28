"""
Здесь реализована случайная генерация для стартовых значений элементов векторов.
У нас есть два вектора значений key_rows, key_columns.
Они используются для создания ключа шифрования
"""
from random import randint
import json
import base64

__all__ = ["KeyManager"]


class KeyManager:
    """
    Данный класс делает так, чтобы ключи изначальные сохранялись файл, который мы можем воспользоваться потом
    Пользователь напросто может забыть входные параметры изображения
    """
    __slots__ = ("_rows", "_columns", "__key_rows_list", "__key_column_list")

    def __init__(self, rows: int, columns: int):
        """
        :param rows: число строк в матрице изображения
        :param columns: число столбцов в матрице изображения
        """
        self._rows = rows
        self._columns = columns
        self.__key_rows_list = self.__key_column_list = None

    @property
    def key_rows(self) -> list[int, ...]:
        """
        Свойство, которое возвращает случайный список чисел, основываясь на количестве строк матрицы.
        Данный список чисел будет использоваться для формирования ключа шифрования.
        """
        if self.__key_rows_list is None:
            self.__key_rows_list = [randint(0, 10000000) for _ in range(self._rows)]
        return self.__key_rows_list

    @property
    def key_columns(self) -> list[int, ...]:
        """
        Свойство, которое возвращает случайный список чисел, основываясь на количестве колонок матрицы.
        Данный список чисел будет использоваться для формирования ключа шифрования.
        """
        if self.__key_column_list is None:
            self.__key_column_list = [randint(0, 10000000) for _ in range(self._columns)]
        return self.__key_column_list

    def __create_cipher_key(self) -> bytes:
        """
        Данный метод используется для создания ключа шифрования
        Он использует два списка и формирует из него ключ шифрования.
        Для реализации будет использоваться json и base64, потому что так нашел в Интернете
        """
        key_dict = {
            "key_rows": self.key_rows,
            "key_columns": self.key_columns
        }

        serialized_key_dict = json.dumps(key_dict)
        return base64.b64encode(serialized_key_dict.encode())

    def create_key_file(self, filename: str = "key.txt"):
        """
        Метод, который сохраняет сгенерированный ключ в бинарный файл
        """
        with open(filename, "wb") as binary_file:
            binary_file.write(self.__create_cipher_key())

    def load_key_file(self, filename: str = "key.txt"):
        """
        Данный метод используется, чтобы узнать ключ шифрования
        Здесь мы разделяем на два вектора для реализации
        """
        with open(filename, "rb") as binary_file:
            encoded_key = binary_file.read()
            decoded_key = base64.b64decode(encoded_key).decode()
            key_dict = json.loads(decoded_key)
            self.__key_rows_list = key_dict["key_rows"]
            self.__key_column_list = key_dict["key_columns"]
