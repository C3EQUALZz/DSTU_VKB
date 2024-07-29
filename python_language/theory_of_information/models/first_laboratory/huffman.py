import heapq
from collections import Counter, namedtuple

from python_language.theory_of_information.core.decorators import loggable


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


class Huffman:

    @staticmethod
    @loggable
    def encode(string: str) -> dict[str, str]:
        queue_with_priority = []
        code = {}

        for char, freq in Counter(string).items():
            queue_with_priority.append((freq, len(queue_with_priority), Leaf(char)))

        heapq.heapify(queue_with_priority)

        count = 0
        while len(queue_with_priority) > 1:
            minimal_frequency, _, left = heapq.heappop(queue_with_priority)
            pre_minimal_freq, _, right = heapq.heappop(queue_with_priority)
            heapq.heappush(queue_with_priority, (minimal_frequency + pre_minimal_freq, count, Node(left, right)))
            count += 1

        if queue_with_priority:
            [(_freq, _count, root)] = queue_with_priority
            root.walk(code, "")

        return code
