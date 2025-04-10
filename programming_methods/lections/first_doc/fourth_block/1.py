# Реверс связного списка
# Определение цикла в связанном списке
# Возврат N элемента из конца в связанном списке
# Удаление дубликатов из связанного списка

from dataclasses import dataclass
from typing import (Callable, Generic, List, Optional, Self, Sequence, TypeVar,
                    Union, overload)

T = TypeVar("T")


@dataclass(slots=True)
class _DoubleNode(Generic[T]):
    """
    Узел двух связного списка.
    """

    item: T
    prev: Optional[Self] = None
    next: Optional[Self] = None


class DoublyLinkedList(Generic[T]):
    """
    Двусвязный список, который является модификацией связного списка.
    Более подробно про двух связные списки можете почитать здесь:
    - https://ru.hexlet.io/courses/basic-algorithms/lessons/double-linked-list/theory_unit
    - https://habr.com/ru/companies/otus/articles/849482/
    """

    @overload
    def __init__(self) -> None: ...

    @overload
    def __init__(self, items: Sequence[T]) -> None: ...

    @overload
    def __init__(self, first: _DoubleNode[T], last: _DoubleNode[T]) -> None: ...

    def __init__(
        self,
        items: Optional[Sequence[T]] = None,
        first: Optional[_DoubleNode[T]] = None,
        last: Optional[_DoubleNode[T]] = None,
    ) -> None:
        self._first: Optional[_DoubleNode[T]]
        self._last: Optional[_DoubleNode[T]]
        self._length: int

        if items is not None:
            self.__initialize_from_items(items)
        elif first is not None and last is not None:
            self.__initialize_from_nodes(first, last)
        else:
            self._first = None
            self._last = None
            self._length = 0

    def __initialize_from_items(self, items: Sequence[T]) -> None:
        """Инициализация списка из коллекции элементов."""
        self._first = None
        self._last = None
        self._length = len(items)

        curr = None
        for item in items:
            if self._first is None:
                self._first = _DoubleNode(item)
                curr = self._first
            else:
                new_node = _DoubleNode(item, curr)
                curr.next = new_node
                curr = new_node
        self._last = curr

    def __initialize_from_nodes(
        self, first: _DoubleNode[T], last: _DoubleNode[T]
    ) -> None:
        """Инициализация списка из указателей на первый и последний узлы."""
        self._first = first
        self._last = last

        count: int = 0
        curr: _DoubleNode[T] = self._first

        while curr is not None:
            count += 1
            curr = curr.next

        self._length: int = count

    def __len__(self) -> int:
        """
        Количество элементов в связном списке
        """
        return self._length

    @overload
    def __getitem__(self, index: int) -> T:
        """
        Метод для получения элемента под индексом.
        Сложность O(n).
        :param index: Индекс, под которым вы хотите получить элемент.
        """
        ...

    @overload
    def __getitem__(self, index: slice) -> Self:
        """
        Метод для получения коллекции элементов с помощью среза.
        В данном случае срез возвращает DoubleLinkedList.
        :param index: Срез - пара вида [start:stop:step]
        """
        ...

    def __getitem__(self, i: Union[int, slice]) -> Union[T, Self]:
        """
        Метод для получения элемента под нужным индексом.
        Здесь сложность O(n).
        """
        if isinstance(i, int):
            if i < 0:
                i = len(self) + i

            if i >= len(self):
                raise IndexError

            # С целью небольшой оптимизации будем идти с разных сторон.
            # Если индекс находится до середины связного списка, то будем начинать с вершины.
            elif i <= len(self) / 2:
                curr: _DoubleNode[T] = self._first
                curr_index: int = 0
                while curr is not None:
                    if i == curr_index:
                        return curr.item
                    curr = curr.next
                    curr_index += 1

            # Если индекс находится после середины, то будем идти с хвоста связного списка.
            elif i >= len(self) / 2:
                curr = self._last
                curr_index = len(self) - 1
                while curr is not None:
                    if i == curr_index:
                        return curr.item
                    curr = curr.prev
                    curr_index -= 1

        elif isinstance(i, slice):
            start: int = i.start
            stop: int = i.stop

            if start is None:
                start = 0
            if stop is None:
                stop = self._length

            if not (0 <= start <= stop <= len(self)):
                raise IndexError("Index must be between 0 and len(self) - 1")
            else:
                new_linked_list: DoublyLinkedList[T] = DoublyLinkedList([])
                index: int = 0

                for item in self:
                    if start <= index < stop:
                        new_linked_list.append(item)
                    index += 1

                return new_linked_list

    def append(self, item: T) -> None:
        """
        Добавить элемент в конец списка.
        """
        new_node: _DoubleNode[T] = _DoubleNode(item, self._last)

        if len(self) == 0:
            self._first = self._last = new_node
            self._length += 1
            return

        self._last.next = new_node
        self._last = new_node
        self._length += 1

    def to_list(self) -> List[T]:
        """
        Возвращает встроенный Python список, содержащий элементы связного списка.
        """
        items_so_far: List[T] = []

        curr: _DoubleNode[T] = self._first
        while curr is not None:
            items_so_far.append(curr.item)
            curr = curr.next

        return items_so_far

    def __contains__(self, item: T) -> bool:
        """
        Проверка наличия элемента в LinkedList.
        В худшем случае O(n).
        :param item: Элемент связного списка, который мы хотим найти.
        """
        if len(self) == 0:
            return False

        elif len(self) % 2 != 0:
            curr_from_start: _DoubleNode[T] = self._first
            curr_from_end: _DoubleNode[T] = self._last

            while curr_from_start != curr_from_end:
                if curr_from_end.item == item or curr_from_start.item == item:
                    return True
                curr_from_start = curr_from_start.next
                curr_from_end = curr_from_end.prev
            if curr_from_start and curr_from_start.item == item:
                return True
            return False
        else:
            if self._first.item == item:
                return True
            curr_from_start = self._first.next
            curr_from_end = self._last

            while curr_from_start != curr_from_end:
                if curr_from_end.item == item or curr_from_start.item == item:
                    return True
                curr_from_start = curr_from_start.next
                curr_from_end = curr_from_end.prev
            if curr_from_start and curr_from_start.item == item:
                return True
            return False

    def insert(self, i: int, item: T) -> None:
        """
        Вставка элемента под нужным индексом в списке.
        Сложность O(n) из-за поиска элемента.

        :param i: Индекс элемента в связном списке.
        :param item: Элемент, который мы хотим вставить.
        """
        if i < 0:
            i = len(self) + i

        if i > len(self):
            raise IndexError(
                "Index out of range. It's bigger than the length of the linked list."
            )

        elif i <= len(self) / 2:
            curr: _DoubleNode[T] = self._first
            curr_index: int = 0

            if i == 0:
                if self._first:
                    new_node: _DoubleNode[T] = _DoubleNode(item, next=self._first)
                    self._first.prev = new_node
                    self._first = new_node
                else:
                    self._first: _DoubleNode[T] = _DoubleNode(item)
                    self._last = self._first
                self._length += 1
                return

            while curr is not None:
                if curr_index == i - 1:
                    new_node: _DoubleNode[T] = _DoubleNode(item, curr, curr.next)
                    if curr.next:
                        curr.next.prev = new_node
                    curr.next = new_node
                    self._length += 1
                    return
                curr = curr.next
                curr_index += 1

        elif i > len(self) / 2:
            curr: _DoubleNode[T] = self._last
            curr_index = len(self) - 1

            while curr is not None:
                if curr_index == i - 1:
                    new_node = _DoubleNode(item, curr, curr.next)
                    if curr.next:
                        curr.next.prev = new_node
                    curr.next = new_node
                    self._length -= 1
                    return
                curr = curr.prev
                curr_index -= 1

    def pop(self, i: int) -> T:
        """
        Удаляет элемент из связного списка.
        :param i: Индекс элемента, который мы хотим удалить. Может быть и отрицательным.
        """
        if i < 0:
            i = len(self) + i

        if i >= len(self):
            raise IndexError(
                "Index out of range. It's bigger than the length of the linked list."
            )

        elif i <= len(self) / 2:
            curr: _DoubleNode[T] = self._first
            curr_index: int = 0

            if i == 0:
                item: T = self._first.item
                self._first = self._first.next

                if self._first:
                    self._first.prev = None

                self._length -= 1
                return item

            while curr is not None:
                if curr_index == i:
                    if curr.next:
                        curr.next.prev = curr.prev
                        if curr.prev:
                            curr.prev.next = curr.next
                    else:
                        if curr.prev:
                            curr.prev.next = None

                    self._length -= 1
                    return curr.item

                curr = curr.next
                curr_index += 1

        elif i > len(self) / 2:
            curr = self._last
            curr_index = len(self) - 1

            if i == curr_index:
                item = self._last.item

                if self._last.prev:
                    self._last.prev.next = None
                    self._last = self._last.prev

                self._length -= 1
                return item

            while curr is not None:
                if curr_index == i:
                    if curr.next:
                        curr.next.prev = curr.prev
                        curr.prev.next = curr.next
                    else:
                        curr.prev.next = None
                    self._length -= 1
                    return curr.item

                curr = curr.prev
                curr_index -= 1

    def __setitem__(self, i: int, item: T) -> None:
        """
        Устанавливает элемент под нужным индексом в связном списке.
        :param i: Индекс элемента в связном списке, должен быть от 0 до длины связного списка.
        """
        current_index: int

        if i < 0:
            i = self._length + i

        if i < (self._length / 2):
            current_index = 0
            curr = self._first

            while curr is not None:
                if current_index == i:
                    curr.item = item

                curr = curr.next
                current_index += 1

        elif i < self._length:
            current_index = self._length - 1
            curr = self._last

            while curr is not None:
                if current_index == i:
                    curr.item = item

                curr = curr.prev
                current_index -= 1
        else:
            raise IndexError(
                "Index is out of range. It must be less than the length of the linked list."
            )

    def index(self, item: T) -> int:
        """
        Возвращает индекс элемента, который вы хотите найти в связном списке.
        :param item: Элемент, который хотите найти.
        :raises: ValueError в случае того, если элемента нет в связном списке.
        """

        index_so_far: int = 0
        curr: _DoubleNode[T] = self._first

        while curr is not None:
            if curr.item == item:
                return index_so_far
            index_so_far += 1
            curr = curr.next
        raise ValueError("Item not found in list.")

    def __str__(self) -> str:
        """
        Возвращает отображение связного списка в виде строки.
        """
        return "[" + " <--> ".join([str(element) for element in self]) + "]"

    def __repr__(self) -> str:
        """
        Возвращает отображение связного списка в виде строки для интерпретатора.
        """
        return f"DoubleLinkedList({self.__str__()})"

    def count(self, item: T) -> int:
        """
        Возвращает количество вхождений элемента в связном списке.
        :param item: Элемент, количество вхождений которого вы хотите узнать.
        :returns: Число вхождений.
        """
        count: int = 0

        if len(self) == 0:
            return count

        curr_from_start: _DoubleNode[T] = self._first
        curr_from_end: _DoubleNode[T] = self._last

        starting_index: int = 0

        if len(self) % 2 == 0:
            starting_index = 1
            curr_from_start = curr_from_start.next

            if self._first.item == item:
                count += 1

        ending_index: int = len(self) - 1

        while starting_index != ending_index:
            if curr_from_start.item == item:
                count += 1
            elif curr_from_end.item == item:
                count += 1

            starting_index += 1
            ending_index -= 1

            curr_from_start = curr_from_start.next
            curr_from_end = curr_from_end.prev

        if curr_from_start.item == curr_from_end.item == item:
            count += 1

        return count

    def copy(self) -> Self:
        """
        Создает поверхностную копию двух связного списка.
        """
        return DoublyLinkedList(first=self._first, last=self._last)

    def __add__(self, other: "DoublyLinkedList[T]") -> Self:
        """
        Магический метод, который определяет поведение
        """
        copy = self.copy()

        curr = other._first

        while curr is not None:
            copy.append(curr.item)
            curr = curr.next

        return copy

    def sort(self, reverse: Optional[bool] = False):
        """
        Сортировка связного списка.
        Здесь не совсем эффективный по памяти, так как мы создаем список,
        его сортируем, а потом на основе его создаем свой новый связный список.
        В результате сложность O(nlog(n)), но по памяти плохо.
        Вручную автор не захотел писать TimSort.
        """
        lst = self.to_list()
        lst.sort(reverse=reverse)
        copy = DoublyLinkedList(lst)
        self._first = copy._first
        self._last = copy._last

    def remove(self, item: T) -> None:
        """
        Удаляет первое вхождение элемент в связном списке.
        :param item: Элемент, который мы хотим удалить в связном списке.
        """
        curr: _DoubleNode[T] = self._first

        if not curr:
            raise ValueError("Cannot remove item from empty list")

        elif curr.item == item:
            self._first = self._first.next

            if self._first:
                self._first.prev = None

            self._length -= 1

        else:
            while curr is not None:
                if curr.next and curr.next.item == item:
                    if curr.next.next:
                        curr.next.next.prev = curr.next
                    curr.next = curr.next.next

                    self._length -= 1
                    return
                curr = curr.next
            raise ValueError

    def __eq__(self, other: "DoublyLinkedList[T]") -> bool:
        """
        Проверяет равны ли связные списки.
        Проверка на равенства
        """
        # Если по длинам не совпадают, то они автоматически уже не равны.
        if len(self) != len(other):
            return False

        curr1: _DoubleNode[T] = self._first
        curr2: _DoubleNode[T] = other._first
        are_equal: bool = True

        while are_equal and curr1 is not None and curr2 is not None:
            if curr1.item != curr2.item:
                are_equal = False
            curr1 = curr1.next
            curr2 = curr2.next

        return are_equal

    def reverse(self) -> None:
        """
        Разворот связного списка.
        Меняет текущий связный список, а не возвращает новый.
        """

        curr = self._first
        previous = None

        while curr:
            curr_value = curr.next
            curr.next = curr.prev
            curr.prev = curr_value

            previous = curr
            curr = curr_value

        self._last = self._first
        self._first = previous

    def extend(self, other: "DoublyLinkedList[T]") -> None:
        """
        Расширяет текущий связный список, благодаря другому.
        Сделано с той целью, чтобы повторить поведение, как у обычного Python
        :param other: Другой связный список, который Вы хотите добавить в текущий.
        Сложность O(m), где m - длина other.
        """
        copy: DoublyLinkedList[T] = self.copy()

        curr: _DoubleNode[T] = other._first

        while curr is not None:
            copy.append(curr.item)
            curr = curr.next

        self._first = copy._first
        self._last = copy._last
        self._length = copy._length

    def has_cycle(self) -> bool:
        """
        Проверка наличия цикла в двусвязном списке.
        Используется алгоритм Флойда ("черепаха и заяц").
        """
        slow = self._first
        fast = self._first

        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next

            if slow is fast:
                return True  # Цикл найден

        return False  # Цикла нет

    def distinct(self) -> None:
        """
        Удаляет все дубликаты из двусвязного списка.
        Сохраняет первое вхождение каждого элемента.
        """
        seen = set()
        current = self._first

        while current is not None:
            item = current.item
            next_node = current.next  # запоминаем следующий узел

            if item in seen:
                self.remove(current.item)
            else:
                seen.add(item)

            current = next_node


def checking_for_reverse() -> None:
    linked_list: DoublyLinkedList[int] = DoublyLinkedList(
        [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    print(f"Изначальный связанный список: {linked_list=}")
    linked_list.reverse()
    print(f"После разворота связанный список: {linked_list=}")


def checking_for_cycle() -> None:
    linked_list: DoublyLinkedList[int] = DoublyLinkedList([1, 2, 3, 4, 5])

    # Пример искусственного создания цикла
    linked_list._last.next = (
        linked_list._first.next
    )  # Последний указывает на второй узел -> цикл

    print(linked_list.has_cycle())  # True


def checking_get_element_from_the_end() -> None:
    linked_list: DoublyLinkedList[int] = DoublyLinkedList([1, 2, 3, 4, 5])
    print(f"Изначальный связанный список: {linked_list=}")
    print(f"Второй элемент с конца: {linked_list[-2]}")


def checking_for_deleting_duplicates() -> None:
    linked_list: DoublyLinkedList[int] = DoublyLinkedList([1, 2, 3, 3, 4, 4, 5])
    print(f"Изначальный связанный список: {linked_list=}")
    linked_list.distinct()
    print(f"Связанный список после удаления дубликатов: {linked_list=}")


def main() -> None:
    functions_for_test: dict[str, Callable[[], None]] = {
        "1": checking_for_reverse,
        "2": checking_for_cycle,
        "3": checking_get_element_from_the_end,
        "4": checking_for_deleting_duplicates,
    }

    while True:
        choice_from_user: str = input(
            "Выберите 1 из 4 варианта для теста связанного списка: "
        )

        if choice_from_user in functions_for_test:
            functions_for_test[choice_from_user]()
            break
        else:
            print("Неправильный выбор")


if __name__ == "__main__":
    main()
