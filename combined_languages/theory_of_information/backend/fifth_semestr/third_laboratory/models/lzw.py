"""
Здесь описан алгоритм LZW

Теоретические материалы:
- https://neerc.ifmo.ru/wiki/index.php?title=%D0%90%D0%BB%D0%B3%D0%BE%D1%80%D0%B8%D1%82%D0%BC_LZW
- https://github.com/adityagupta3006/LZW-Compressor-in-Python

Важный момент: алгоритм LZW не обеспечивает сжатие полноценно, в результате может выйти файл, который больше по размеру
"""
from combined_languages.theory_of_information.backend.core.decorators import loggable
from combined_languages.theory_of_information.backend.core.abstract_classes import Compressor
import struct


class LZW(Compressor):
    def __init__(self) -> None:
        self.DICTIONARY_SIZE: int = 114112
        self.maximum_table_size: int = pow(2, int(self.DICTIONARY_SIZE))

    @loggable
    def compress(self, data: str) -> bytes:
        """
        Здесь происходит логика сжатия данных
        """
        dictionary_size = self.DICTIONARY_SIZE

        dictionary = {chr(i): i for i in range(self.DICTIONARY_SIZE)}

        string = ""
        compressed_data = []

        for symbol in data:
            string_plus_symbol = string + symbol
            if string_plus_symbol in dictionary:
                string = string_plus_symbol
            else:
                compressed_data.append(dictionary[string])
                if len(dictionary) <= self.maximum_table_size:
                    dictionary[string_plus_symbol] = dictionary_size
                    dictionary_size += 1
                string = symbol

        if string in dictionary:
            compressed_data.append(dictionary[string])

        return b"".join(struct.pack('>H', int(data)) for data in compressed_data)

    @loggable
    def decompress(self, compressed_data: bytes) -> str:
        # Building and initializing the dictionary.
        dictionary = {x: chr(x) for x in range(self.DICTIONARY_SIZE)}

        # Reading the compressed data.
        compressed_data = [int.from_bytes(compressed_data[i:i + 2], 'big') for i in range(0, len(compressed_data), 2)]

        # LZW Decompression algorithm
        next_code = 256
        decompressed_data = ""
        string = ""

        for code in compressed_data:
            if not (code in dictionary):
                dictionary[code] = string + (string[0])
            decompressed_data += dictionary[code]
            if not (len(string) == 0):
                dictionary[next_code] = string + (dictionary[code][0])
                next_code += 1
            string = dictionary[code]

        return decompressed_data

if __name__ == "__main__":
    compressor = LZW()
    a = compressor.compress("Привет, мир!")
    print(a)
    b = compressor.decompress(a)
    print(b)