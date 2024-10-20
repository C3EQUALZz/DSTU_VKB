import heapq
from collections import Counter, namedtuple

from combined_languages.theory_of_information.backend.core.decorators import loggable


class Leaf(namedtuple('Leaf', 'char')):
    @loggable
    def walk(self, code: dict[str, str], acc: str) -> None:
        code[self.char] = acc or "0"


class Node(namedtuple('Node', ["left", "right"])):
    @loggable
    def walk(self, code: dict[str, str], acc: str) -> None:
        """
        :param code:
        :param acc: префикс кода, который мы накопили, спускаясь от корня до данного узла или листа
        """
        self.left.walk(code, acc + "0")
        self.right.walk(code, acc + "1")


class Tree:
    def __init__(self, dictionary_with_freq: dict[str, float]) -> None:
        self.dictionary_with_freq = dictionary_with_freq

    # noinspection PyMethodMayBeStatic
    def build(self) -> dict[str, str]:
        """
        Построение дерева Хаффмана, чтобы в дальнейшем закодировать слово
        """
        queue_with_priority = []
        code = {}

        for char, freq in self.dictionary_with_freq.items():
            queue_with_priority.append((freq, len(queue_with_priority), Leaf(char)))

        heapq.heapify(queue_with_priority)

        count = 0
        while len(queue_with_priority) > 1:
            minimal_frequency, _, left = heapq.heappop(queue_with_priority)
            _, pre_minimal_freq, right = heapq.heappop(queue_with_priority)
            heapq.heappush(queue_with_priority, (minimal_frequency + pre_minimal_freq, count, Node(left, right)))
            count += 1

        if queue_with_priority:
            [(_freq, _count, root)] = queue_with_priority
            root.walk(code, "")

        return code


class Huffman:
    def __init__(self, tree: Tree) -> None:
        self.tree = tree.build()

    @loggable
    def encode(self, string: str) -> str:
        return "".join(self.tree[char] for char in string)

    @loggable
    def decode(self, encoded_string: str) -> str:
        """
        Метод для декодирования последовательности символов.
        :param encoded_string: Закодированное слово, которое нужно вернуть в исходное.
        :param code: Таблица символов соответствия (дерево - Хаффмана), где каждому символу вы назначили код
        """
        reverse_code = {v: k for k, v in self.tree.items()}
        decoded_string = ""
        temp = ""

        for bit in encoded_string:
            temp += bit
            if temp in reverse_code:
                decoded_string += reverse_code[temp]
                temp = ""

        return decoded_string


if __name__ == "__main__":
    word = "Привет, мир!"
    map_with_freq = {char: count / len(word) for char, count in Counter(word).items()}
    tree = Tree(map_with_freq)
    print(tree.build())
    coder = Huffman(tree)
    encoded = coder.encode(word)
    print(encoded)
    decoded = coder.decode(encoded)
    print(decoded)
