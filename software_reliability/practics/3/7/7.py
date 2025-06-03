"""
Вариант 7 Определить понятие «Книга». Состояние объекта определяется следующими полями:
• единый регистрационный номер (длинное целое число);
• автор (строка до 20 символов);
• год издания (целое число);
• количество экземпляров (целое число).
Вычислить количество экземпляров книг заданного автора, выпущенных в период с 2007 по 2016 г.
"""

from abc import abstractmethod
from typing import Protocol, List, override


class Book(Protocol):
    @property
    @abstractmethod
    def reg_number(self) -> int:
        raise NotImplementedError

    @reg_number.setter
    @abstractmethod
    def reg_number(self, value: int) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def author(self) -> str:
        raise NotImplementedError

    @author.setter
    @abstractmethod
    def author(self, value: str) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def year(self) -> int:
        raise NotImplementedError

    @year.setter
    @abstractmethod
    def year(self, value: int) -> None:
        raise NotImplementedError

    @property
    @abstractmethod
    def copies(self) -> int:
        raise NotImplementedError

    @copies.setter
    @abstractmethod
    def copies(self, value: int) -> None:
        raise NotImplementedError


class SimpleBook(Book):
    def __init__(self, reg_number: int, author: str, year: int, copies: int) -> None:
        self.reg_number: int = reg_number
        self.author: str = author
        self.year: int = year
        self.copies: int = copies

    @property
    @override
    def reg_number(self) -> int:  # type: ignore
        return self._reg_number

    @reg_number.setter
    @override
    def reg_number(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Регистрационный номер должен быть положительным")
        self._reg_number: int = value

    @property
    @override
    def author(self) -> str:  # type: ignore
        return self._author

    @author.setter
    @override
    def author(self, value: str) -> None:
        if len(value) > 20:
            raise ValueError("Имя автора не должно превышать 20 символов")
        self._author: str = value

    @property
    @override
    def year(self) -> int:  # type: ignore
        return self._year

    @year.setter
    @override
    def year(self, value: int) -> None:
        if not (2007 <= value <= 2016):
            raise ValueError("Год издания должен быть между 2007 и 2016")
        self._year: int = value

    @property
    @override
    def copies(self) -> int:  # type: ignore
        return self._copies

    @copies.setter
    @override
    def copies(self, value: int) -> None:
        if value < 0:
            raise ValueError("Количество экземпляров не может быть отрицательным")
        self._copies: int = value


class BookManager:
    def __init__(self) -> None:
        self._books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def count_books_by_author_and_period(self, target_author: str) -> int:
        count = 0
        for book in self._books:
            if book.author == target_author and 2007 <= book.year <= 2016:
                count += book.copies
        return count


def main() -> None:
    manager: BookManager = BookManager()

    try:
        n: int = int(input("Введите количество книг: "))

        for i in range(n):
            while True:
                try:
                    reg_number: int = int(input(f"Книга {i + 1}. Регистрационный номер: "))
                    author: str = input("Автор: ")
                    year: int = int(input("Год издания: "))
                    copies: int = int(input("Количество экземпляров: "))

                    book: SimpleBook = SimpleBook(reg_number, author, year, copies)
                    manager.add_book(book)
                    break
                except ValueError as e:
                    print(f"Ошибка ввода: {e}. Повторите ввод.")

        target_author: str = input("\nВведите имя автора для подсчёта: ")
        total_copies: int = manager.count_books_by_author_and_period(target_author)

        print(f"\nКоличество экземпляров книг автора {target_author} (2007-2016): {total_copies}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
