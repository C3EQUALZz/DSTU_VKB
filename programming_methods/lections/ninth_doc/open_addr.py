from typing import TypeVar, Optional, Tuple, List, override

from programming_methods.lections.ninth_doc.base import BaseDict

K = TypeVar('K')
V = TypeVar('V')


class OpenAddrDict(BaseDict[K, V]):
    _DELETED = object()

    def __init__(self, initial_size: int = 8, load_factor: float = 0.75) -> None:
        super().__init__(initial_size, load_factor)
        self.table: List[Optional[Tuple[K, V] | object]] = [None] * self.size
        self._num_deleted = 0

    @override
    def _resize(self, new_size: int) -> None:
        old_table = self.table
        self.size = new_size
        self.table = [None] * self.size
        self._count = 0
        self._num_deleted = 0

        for entry in old_table:
            if entry is not None and entry is not self._DELETED:
                key, value = entry  # type: ignore
                self[key] = value

    @override
    def _find_index(self, key: K) -> Tuple[Optional[int], bool]:
        index = self._hash(key)
        first_deleted: Optional[int] = None

        for i in range(self.size):
            current_index = (index + i) % self.size
            entry = self.table[current_index]

            if entry is None:
                return current_index, False

            if entry is self._DELETED:
                if first_deleted is None:
                    first_deleted = current_index
                continue

            entry_key, _ = entry  # type: ignore
            if entry_key == key:
                return current_index, True

        return (first_deleted, False) if first_deleted else (None, False)

    @override
    def __setitem__(self, key: K, value: V) -> None:
        if (self._count + 1) / self.size > self.load_factor:
            self._resize(self.size * 2)

        index, found = self._find_index(key)

        if index is None:
            raise RuntimeError("Хеш-таблица переполнена")

        if not found and self.table[index] is self._DELETED:
            self._num_deleted -= 1

        self.table[index] = (key, value)
        self._count += int(not found)

    @override
    def __getitem__(self, key: K) -> V:
        index, found = self._find_index(key)
        if not found or index is None:
            raise KeyError(key)
        return self.table[index][1]  # type: ignore

    @override
    def __delitem__(self, key: K) -> None:
        index, found = self._find_index(key)
        if not found or index is None:
            raise KeyError(key)
        self.table[index] = self._DELETED
        self._count -= 1
        self._num_deleted += 1

    @override
    def __contains__(self, key: K) -> bool:
        _, found = self._find_index(key)
        return found


def main() -> None:
    # Пример использования с типами
    d: OpenAddrDict[str, int] = OpenAddrDict()
    d["apple"] = 5
    d["banana"] = 7
    print(d["apple"])  # 5
    del d["apple"]
    print("apple" in d)  #


if __name__ == "__main__":
    main()
