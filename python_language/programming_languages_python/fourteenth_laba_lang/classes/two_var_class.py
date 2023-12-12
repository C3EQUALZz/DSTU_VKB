"""
Данный модуль описывает задание по созданию класса с двумя координатами
"""

StringInt = int | str


class TwoVariables:
    def __init__(self, x: StringInt, y: StringInt):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def modify(self, new_value1: StringInt, new_value2: StringInt):
        self.x = new_value1
        self.y = new_value2

    def sum(self) -> StringInt:
        return self.x + self.y

    def max_variable(self) -> StringInt:
        return max(self.x, self.y)
