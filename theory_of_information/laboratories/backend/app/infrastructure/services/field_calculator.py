class FieldCalculatorService:
    def evaluate_expression(self, rpn_expr: list[int | str], mod: int) -> int:
        """Вычисляет выражение, записанное в обратной польской нотации"""
        stack: list[int] = []

        for token in rpn_expr:
            if isinstance(token, int):
                stack.append(token % mod)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(self.__apply_operation(a, b, token, mod))

        return stack[0]

    def __apply_operation(self, a: int, b: int, op: str, mod: int):
        """Применяет арифметическую операцию в поле Z/modZ"""
        if op == '+':
            return (a + b) % mod
        if op == '-':
            return (a - b) % mod
        if op == '*':
            return (a * b) % mod
        if op == '/':
            return (a * self.__mod_inverse(b, mod)) % mod
        if op == '^':
            return pow(a, b, mod)  # Быстрое возведение в степень
        raise ValueError(f"Неизвестная операция {op}")

    def __mod_inverse(self, a: int, mod: int) -> int:
        """Находит мультипликативно обратный элемент a^(-1) по модулю mod"""
        g, x, _ = self.__extended_gcd(a, mod)
        if g != 1:
            raise ValueError(f"Число {a} не имеет обратного по модулю {mod}")
        return x % mod

    @staticmethod
    def __extended_gcd(a: int, b: int) -> tuple[int, int, int]:
        """Расширенный алгоритм Евклида для нахождения обратного элемента"""
        old_r, r = a, b
        old_s, s = 1, 0
        old_t, t = 0, 1

        while r:
            quotient = old_r // r
            old_r, r = r, old_r - quotient * r
            old_s, s = s, old_s - quotient * s
            old_t, t = t, old_t - quotient * t

        return old_r, old_s, old_t  # gcd, x, y