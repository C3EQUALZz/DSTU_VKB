# Реализация двух стеков в массиве

class TwoStacks:
    def __init__(self, n: int = 10) -> None:
        # инициализировать массив и верхний индекс для каждого стека
        self.arr = [0] * n
        self.top1 = -1
        self.top2 = n

    def push_to_first(self, x) -> None:
        # проверьте, есть ли место для нового элемента
        if self.top1 < self.top2 - 1:
            # увеличить верхний индекс первого стека
            self.top1 += 1
            # добавить элемент в массив
            self.arr[self.top1] = x
        else:
            # стек заполнен, генерировать исключение
            raise Exception("Stack Overflow")

    def push_to_second(self, x) -> None:
        # проверьте, есть ли место для нового элемента
        if self.top1 < self.top2 - 1:
            # уменьшить верхний индекс второго стека
            self.top2 -= 1
            # добавить элемент в массив
            self.arr[self.top2] = x
        else:
            # стек заполнен, генерировать исключение
            raise Exception("Stack Overflow")

    def __str__(self) -> str:
        return f"First stack: {self.arr[:self.top1 + 1]}, Second stack: {self.arr[self.top2:]}"


if __name__ == "__main__":
    two = TwoStacks()
    two.push_to_first(1)
    two.push_to_second(2)
    print(two)
