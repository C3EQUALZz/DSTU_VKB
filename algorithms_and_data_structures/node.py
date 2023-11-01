"""
Класс для реализации точек (узлов односвязного списка)
Здесь реализованы методы:
    - Получение веса текущего узла;
    - Получение веса следующего узла;
    - Установка веса текущего узла;
    - Установка веса следующего узла;
"""


class Node:
    def __init__(self, data=0, next_data=None):
        self.data = data
        self.next_data = next_data

    def get_current(self):
        return self.data

    def get_next(self):
        return self.next_data

    def set_current(self, data):
        self.data = data

    def set_next(self, data):
        self.next_data = data