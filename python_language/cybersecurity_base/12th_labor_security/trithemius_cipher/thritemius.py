import re
from .enums import Letters
from functools import reduce


class TrisemusCipher:
    def __init__(self, key: str, table_sizes: str):
        self.key = key
        self.table_sizes = re.split(r"x|,|\s", table_sizes)
        self.size = reduce(lambda x, y: int(x) * int(y), self.table_sizes, 1)

    def encode(self, string: str):
        key = ''.join(sorted(set(self.key), key=self.key.index))
        table = (key + ''.join(x for x in TrisemusCipher._get_language(string) if x not in key))[:self.size]
        return ''.join(self._encode_symbol(x, table) if x.isalpha() else x for x in string)

    def decode(self, string: str):
        key = ''.join(sorted(set(self.key), key=self.key.index))
        table = (key + ''.join(x for x in TrisemusCipher._get_language(string) if x not in key))[:self.size]
        return ''.join(self._decode_symbol(x, table) if x.isalpha() else x for x in string)

    def _encode_symbol(self, char: str, table: str):
        return table[(table.find(char) + int(self.table_sizes[-1])) % len(table)]

    def _decode_symbol(self, char: str, table: str):
        return table[(table.find(char) - int(self.table_sizes[-1])) % len(table)]

    @staticmethod
    def _get_language(string: str) -> str:
        words = re.findall(r'\w+', string, re.UNICODE)
        if all(re.fullmatch(r"^[a-z]+$", word) for word in words):
            return Letters.ENGLISH_SYMBOLS_LOWER.value
        if all(re.fullmatch(r"^[а-яё]+$", word) for word in words):
            return Letters.RUSSIAN_SYMBOLS_LOWER.value
        if all(re.fullmatch(r"^[A-Z]+$", word) for word in words):
            return Letters.ENGLISH_SYMBOLS_UPPER.value
        if all(re.fullmatch(r"^[А-ЯЁ]+$", word) for word in words):
            return Letters.RUSSIAN_SYMBOLS_UPPER.value
