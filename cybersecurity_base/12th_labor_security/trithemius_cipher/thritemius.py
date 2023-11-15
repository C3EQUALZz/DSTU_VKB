"""
Оригинал взят отсюда: https://github.com/5x/cryptography-gui-app
TODO: разобраться и поправить код
"""
from abc import ABCMeta, abstractmethod

from .cipher_abc import CipherABC
from .alphabet import get_alphabet
from .utils.expr_parser import prepare_expression


class TrithemiusHandleABC(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get_code(self, index):
        pass


class LinearEquationException(Exception):
    pass


class TrithemiusLinearEquation(TrithemiusHandleABC):
    def __init__(self, symbols_collection, key, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.expr = prepare_expression(key)

    def get_code(self, index):
        try:
            value = self.expr(t=index)
        except TypeError as e:
            raise TypeError(e)
        except SyntaxError as e:
            raise SyntaxError(e)
        except Exception as e:
            raise LinearEquationException(e)

        return value


class TrithemiusAssocReplace(TrithemiusHandleABC):
    def __init__(self, symbols_collection, key, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.key_len = len(key)
        self.assoc_map = self.create_assoc(key, symbols_collection)

    def get_code(self, index):
        key_index = index % self.key_len
        msg_index = self.assoc_map.get(key_index, index)

        return msg_index

    @staticmethod
    def create_assoc(key, symbols_collection):
        assoc_map = dict()

        for index in range(len(key)):
            key_chr = key[index]

            if key_chr in symbols_collection:
                value = symbols_collection.find(key_chr)
                assoc_map[index] = value

        return assoc_map


class TrithemiusCipher(CipherABC):
    def __init__(self, key, handle, alphabet='EN'):
        super().__init__(key)

        alphabet_symbols = get_alphabet(alphabet)
        self.symbols_collection = "".join(alphabet_symbols)
        self._handle = handle

    @property
    def handle(self):
        return self._handle(self.symbols_collection, self.key)

    def encrypt(self, plain_text):
        get_code = self.handle.get_code
        return self._replace_chars(plain_text, lambda i: get_code(i))

    def decrypt(self, cipher_text):
        get_code = self.handle.get_code
        return self._replace_chars(cipher_text, lambda i: -(get_code(i)))

    def _replace_chars(self, msg, func):
        assoc_map = self._assoc_map()
        symbols_count = len(self.symbols_collection)

        res = []
        for index, char in enumerate(msg):
            char_index = assoc_map.get(char, None)

            if char_index is not None:
                new_index = (char_index + func(index + 1)) % symbols_count
                char = self.symbols_collection[new_index]

            res.append(char)

        return "".join(res)

    def _assoc_map(self):
        return {j: i for i, j in enumerate(self.symbols_collection)}


if __name__ == "__main__":
    cipher = TrithemiusCipher("my secret key", TrithemiusAssocReplace)
    crt_text = cipher.encrypt("the quick brown fox jumps over the lazy dog.")
    plain_text = cipher.decrypt(crt_text)

    print(crt_text)
    print(plain_text)