from typing import List, Tuple, TypeVar, override

from programming_methods.lections.ninth_doc.base import BaseDict

K = TypeVar('K')
V = TypeVar('V')


class ChainingDict(BaseDict[K, V]):
    def __init__(self, initial_size: int = 8, load_factor: float = 0.75) -> None:
        super().__init__(initial_size=initial_size, load_factor=load_factor)
        self.table: List[List[Tuple[K, V]]] = [[] for _ in range(self.size)]

    @override
    def _resize(self, new_size: int) -> None:
        old_table = self.table
        self.size = new_size
        self.table = [[] for _ in range(self.size)]
        self._count = 0

        for bucket in old_table:
            for key, value in bucket:
                self[key] = value

    @override
    def __setitem__(self, key: K, value: V) -> None:
        if self._count / self.size > self.load_factor:
            self._resize(self.size * 2)

        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, _) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))
        self._count += 1

    @override
    def __getitem__(self, key: K) -> V:
        index = self._hash(key)
        for k, v in self.table[index]:
            if k == key:
                return v
        raise KeyError(key)

    @override
    def __delitem__(self, key: K) -> None:
        index = self._hash(key)
        bucket = self.table[index]
        for i, (k, _) in enumerate(bucket):
            if k == key:
                del bucket[i]
                self._count -= 1
                return
        raise KeyError(key)

    @override
    def __contains__(self, key: K) -> bool:
        index = self._hash(key)
        return any(k == key for k, _ in self.table[index])

    @override
    def items(self) -> List[Tuple[K, V]]:
        return [item for bucket in self.table for item in bucket]


def main() -> None:
    # Пример использования
    d: ChainingDict[str, int] = ChainingDict()
    d["apple"] = 5
    d["banana"] = 7
    d["apple"] = 10  # Обновление значения

    print(d["apple"])  # 10
    print(len(d))  # 2
    del d["banana"]
    print("banana" in d)  # False

    # Коллизия (для демонстрации)
    d2: ChainingDict[int, str] = ChainingDict(4)
    d2[0] = "zero"
    d2[4] = "four"  # Та же ячейка (4 % 4 == 0)
    print(d2.items())  # [(0, 'zero'), (4, 'four')]


if __name__ == "__main__":
    main()
