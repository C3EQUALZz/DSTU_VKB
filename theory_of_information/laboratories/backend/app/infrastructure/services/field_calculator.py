from app.domain.entities.calculator import FieldCalculator


class FieldCalculatorService:
    @staticmethod
    def evaluate_expression(rpn_expr: list[int | str], mod: int) -> int:
        """Вычисляет выражение, записанное в обратной польской нотации"""
        stack: list[int] = []
        calculator: FieldCalculator = FieldCalculator()

        for token in rpn_expr:
            if isinstance(token, int):
                stack.append(token % mod)
            else:
                b = stack.pop()
                a = stack.pop()
                stack.append(calculator.apply_operation(a, b, token, mod))

        return stack[0]
