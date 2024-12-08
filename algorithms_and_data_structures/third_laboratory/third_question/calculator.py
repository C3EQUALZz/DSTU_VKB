def evaluate_rpn(expression: str) -> float:
    """Вычисляет значение выражения в обратной польской записи (ОПН)."""
    stack = []
    tokens = expression.split()

    for token in tokens:
        if token.isdigit() or (token[0] == '-' and token[1:].isdigit()):  # Проверка на целое число
            stack.append(float(token))  # Добавляем операнды в стек
        else:
            # Извлекаем два верхних операнда из стека
            right_operand = stack.pop()
            left_operand = stack.pop()

            if token not in {"+", "-", "*", "/"}:
                raise ValueError(f"Неизвестная операция: {token}")

            stack.append(eval(f"{left_operand} {token} {right_operand}"))

    # В конце в стеке должен остаться один элемент - результат
    return stack.pop()
