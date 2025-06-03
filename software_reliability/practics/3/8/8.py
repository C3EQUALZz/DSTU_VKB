"""
Вариант 8. Определить понятие «Книга». Состояние объекта определяется следующими полями:
• единый регистрационный номер (длинное целое число);
• автор (строка до 20 символов);
• год издания (целое число);
• количество страниц (целое число).
Вычислить средний объем книги в страницах среди книг, выпущенных за заданный период времени.
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
    def pages(self) -> int:
        raise NotImplementedError

    @pages.setter
    @abstractmethod
    def pages(self, value: int) -> None:
        raise NotImplementedError


class SimpleBook(Book):
    def __init__(self, reg_number: int, author: str, year: int, pages: int) -> None:
        self.reg_number: int = reg_number
        self.author: str = author
        self.year: int = year
        self.pages: int = pages

    @property
    @override
    def reg_number(self) -> int:  # type: ignore
        return self._reg_number

    @reg_number.setter
    def reg_number(self, value: int) -> None:
        if value <= 0:
            raise ValueError("Регистрационный номер должен быть положительным")
        self._reg_number = value

    @property
    def author(self) -> str:  # type: ignore
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        if len(value) > 20:
            raise ValueError("Имя автора не должно превышать 20 символов")
        self._author = value

    @property
    def year(self) -> int:  # type: ignore
        return self._year

    @year.setter
    def year(self, value: int) -> None:
        if not (1800 <= value <= 2023):
            raise ValueError("Год издания должен быть в диапазоне 1800–2023")
        self._year = value

    @property
    def pages(self) -> int:  # type: ignore
        return self._pages

    @pages.setter
    def pages(self, value: int) -> None:
        if value < 0:
            raise ValueError("Количество страниц не может быть отрицательным")
        self._pages = value


class BookManager:
    def __init__(self) -> None:
        self._books: List[Book] = []

    def add_book(self, book: Book) -> None:
        self._books.append(book)

    def average_pages_in_period(self, start_year: int, end_year: int) -> float:
        filtered_books = [
            book for book in self._books
            if start_year <= book.year <= end_year
        ]
        if not filtered_books:
            return 0.0
        total_pages: int = sum(book.pages for book in filtered_books)
        return total_pages / len(filtered_books)


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
                    pages: int = int(input("Количество страниц: "))

                    book: SimpleBook = SimpleBook(reg_number, author, year, pages)
                    manager.add_book(book)
                    break
                except ValueError as e:
                    print(f"Ошибка ввода: {e}. Повторите ввод.")

        print("\nВведите период для расчёта среднего количества страниц:")
        start_year: int = int(input("Начальный год: "))
        end_year: int = int(input("Конечный год: "))

        avg_pages: float = manager.average_pages_in_period(start_year, end_year)

        if avg_pages == 0.0:
            print("\nНет книг, выпущенных в указанный период.")
        else:
            print(f"\nСреднее количество страниц в книгах ({start_year}–{end_year}): {avg_pages:.2f}")

    except ValueError as e:
        print(f"Ошибка ввода: {e}")


if __name__ == "__main__":
    main()
