import re
from collections import deque
from typing import Final

from app.infrastructure.services.field_calculator import FieldCalculatorService
from app.logic.commands.field_calculator import EvaluateExpressionInField
from app.logic.use_cases.base import BaseUseCase


class EvaluateMathExpressionInFieldUseCase(BaseUseCase[EvaluateExpressionInField]):
    # Приоритет операторов
    OPERATOR_PRECEDENCE: Final[dict[str, int]] = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }

    def __init__(self, service: FieldCalculatorService) -> None:
        self.service = service

    async def __call__(self, command: EvaluateExpressionInField) -> int:
        """Преобразует инфиксное выражение в обратную польскую нотацию (RPN)"""
        output: list[str | int] = []
        operators: deque[str] = deque()

        expression = command.expression
        mod = command.mod

        tokens = re.findall(r'\d+|[+\-*/^()]', expression)
        for token in tokens:
            if token.isdigit():
                output.append(int(token))
            elif token in self.OPERATOR_PRECEDENCE:
                while (operators and operators[-1] != '(' and
                       self.OPERATOR_PRECEDENCE[operators[-1]] >= self.OPERATOR_PRECEDENCE[token]):
                    output.append(operators.pop())
                operators.append(token)
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators and operators[-1] != '(':
                    output.append(operators.pop())
                operators.pop()  # Удаляем '('

        while operators:
            output.append(operators.pop())

        return self.service.evaluate_expression(output, mod)
