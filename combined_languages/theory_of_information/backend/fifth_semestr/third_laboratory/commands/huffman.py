import io
import pickle

from combined_languages.theory_of_information.backend.core.abstract_classes import Command
from combined_languages.theory_of_information.backend.fifth_semestr.third_laboratory.models.huffman import Huffman, Tree
from collections import Counter



class EncodeCommand(Command):
    def __init__(self, data: str) -> None:
        self.data = data

    def execute(self) -> tuple[str, bytes]:
        map_with_freq = {char: count / len(self.data) for char, count in Counter(self.data).items()}
        tree = Tree(map_with_freq)

        huffman = Huffman(tree)

        encoded = huffman.encode(self.data)

        result_data = {
            'encoded': encoded,
            'frequencies': map_with_freq
        }

        return str(tree.build()), pickle.dumps(result_data)


class DecodeCommand(Command):
    def __init__(self, data: bytes) -> None:
        self.data = data

    def execute(self) -> tuple[str, io.BytesIO]:
        encoded, map_with_freq = pickle.loads(self.data).values()
        tree = Tree(map_with_freq)

        huffman = Huffman(tree)

        decoded = huffman.decode(encoded)

        return str(tree.build()), io.BytesIO(decoded.encode("utf-8"))
