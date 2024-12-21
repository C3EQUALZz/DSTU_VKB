"""
Класс, который описывает библиотеку
"""
from dataclasses import dataclass
from typing import TypeVar

from prettytable import PrettyTable

Book = TypeVar('Book')


@dataclass
class Book:
    """
    Данный класс описывает книгу
    """
    title: str
    author: str
    year: int

    @classmethod
    def from_string(cls, string: str) -> Book:
        return Book(*string.split())

class Library:
    """
    Данный класс описывает библиотеку книг
    """

    def __init__(self, books=None) -> None:
        self.books = [] if books is None else books

    def append(self, book: str) -> None:
        """
        Метод, который добавляет книгу в библиотеку
        """
        self.books.append(Book.from_string(book))

    def remove(self, title: str) -> None:
        """
        Метод, который удаляет книгу
        """
        for index, book in enumerate(self.books):
            if book.title == title.split()[0]:
                self.books.pop(index)

    def search_books(self, key, value) -> list:
        """
        Метод, который ищет книгу по названию
        """
        return [book for book in self.books if str(getattr(book, key, None)) == str(value)]

    def sort_books(self, key) -> list:
        """
        Метод, который сортирует по ключу
        """
        return sorted(self.books, key=key)

    def to_pretty_table(self) -> PrettyTable:
        """
        Метод для вывода данных о библиотеке
        """
        table = PrettyTable()
        table.field_names = ["Название", "Автор", "Год написания"]
        table.add_rows([[book.title, book.author, book.year] for book in self.books])
        return table
