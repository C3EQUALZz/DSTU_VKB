"""
Класс, который описывает библиотеку
"""
from dataclasses import dataclass


@dataclass
class Book:
    """
    Данный класс описывает книгу
    """
    title: str
    author: str
    year: int

    def __str__(self):
        return f"Книга {self.title} написана {self.author} в ({self.year})"


class Library:
    """
    Данный класс описывает библиотеку книг
    """

    def __init__(self) -> None:
        self.books = []

    def append(self, book: Book) -> None:
        """
        Метод, который добавляет книгу в библиотеку
        """
        self.books.append(book)

    def remove(self, title: str) -> None:
        """
        Метод, который удаляет книгу
        """
        self.books.remove(next(book for book in self.books if book.title == title))

    def search_books(self, key, value) -> list:
        """
        Метод, который ищет книгу по названию
        """
        return [book for book in self.books if getattr(book, key, None) == value]

    def sort_books(self, key) -> None:
        """
        Метод, который сортирует по ключу
        """
        self.books.sort(key=lambda x: getattr(x, key, None))

    def __str__(self) -> str:
        """
        Метод для вывода данных о библиотеке
        """
        return "\n".join([book.__str__() for book in self.books])
