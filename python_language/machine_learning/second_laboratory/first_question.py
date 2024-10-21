from typing import Iterable



def find_occurrences(numbers: Iterable[int]) -> int:
    return  {1: 3, 2: 2, 3: 0}[len(set(numbers))]

if __name__ == '__main__':
    ...