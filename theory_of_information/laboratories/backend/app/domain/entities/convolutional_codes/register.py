from collections import deque
from dataclasses import dataclass
from itertools import accumulate
from operator import xor
from typing import Sequence

from app.domain.entities.base import BaseEntity


@dataclass(eq=False)
class Register(BaseEntity):
    indexes: list[int]

    def apply(self, data: Sequence[int]) -> int:
        filtered_data = [data[i] for i in self.indexes]
        result_iter = accumulate(filtered_data, xor)
        return list(result_iter)[-1]


@dataclass(eq=False)
class PolsCalculator(BaseEntity):
    data: str
    indexes_for_sum: list[list[int]]

    def apply(self) -> str:
        count_of_registers = 3
        queue: deque[int] = deque(maxlen=count_of_registers)
        registers: list[Register] = [Register(index) for index in self.indexes_for_sum]
        pols = []

        for _ in range(count_of_registers):
            queue.append(0)

        for number in self.data:
            queue.appendleft(int(number))
            print(queue)
            pols.append("".join(str(register.apply(queue)) for register in registers))

        return ",".join(pols)


if __name__ == "__main__":
    i = "1101"
    indexes = [[0, 1, 2], [0, 2]]
    calc = PolsCalculator(i, indexes)
    print(calc.apply())
